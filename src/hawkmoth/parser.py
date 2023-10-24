# Copyright (c) 2016-2017 Jani Nikula <jani@nikula.org>
# Copyright (c) 2018-2023 Bruno Santos <brunomanuelsantos@tecnico.ulisboa.pt>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.
"""
Documentation comment extractor
===============================

This module extracts relevant documentation comments.

This is the part that uses Clang Python Bindings to extract documentation
comments from C source code. This module does not depend on Sphinx.

There are two passes:

#. Pass over the tokens to find all the comments, including ones that aren't
   attached to cursors.

#. Pass over the cursors to document them.

There is minimal syntax parsing or input conversion:

* Identification of documentation comment blocks, i.e. comments that start
  with ``/**``.

* Identification of function-like macros.

* Identification of array and function pointer variables, members and
  arguments, and conversion to a format suitable for Sphinx C Domain.

The documentation comments are returned verbatim in a tree of Docstring objects.
"""

import enum
import os
from dataclasses import dataclass

from clang.cindex import TokenKind, CursorKind
from clang.cindex import Index, TranslationUnit, TranslationUnitLoadError
from clang.cindex import Diagnostic

from hawkmoth import docstring
from hawkmoth.commentedcursor import (
    _cursor_get_tokens,
    _get_meta,
    CompoundDecl,
    EnumConstantDecl,
    FunctionDecl,
    MacroDefinition,
    MethodDecl,
    TopLevelComment,
    TypedefDecl,
    VarFieldDecl,
)

class ErrorLevel(enum.IntEnum):
    """
    Supported error levels. The values are an implementation detail.
    """
    DEBUG = Diagnostic.Ignored
    INFO = Diagnostic.Note
    WARNING = Diagnostic.Warning
    ERROR = Diagnostic.Error
    CRITICAL = Diagnostic.Fatal

@dataclass
class ParserError:
    level: ErrorLevel
    filename: str
    line: int
    message: str

    def get_message(self):
        if self.filename:
            if self.line is not None:
                return f'{self.filename}:{self.line}: {self.message}'
            else:
                return f'{self.filename}: {self.message}'
        else:
            return f'{self.message}'

def _domain_is_valid(tu, domain, errors):
    """Check the derived domain of a translation unit against the expected one.

    The derived domain is observed indirectly by the definition of certain C++
    specific macros. We try to maximize our chances by looking for any of the
    known macros in case any of them is disabled through compiler flags or
    preprocessor statements.
    """
    cpp_macros = (
        '__cpp_rtti',
        '__cpp_exceptions',
        '__cpp_unicode_characters',
        '__cpp_raw_strings',
        '__cpp_unicode_literals',
        '__cpp_user_defined_literals',
        '__cpp_lambdas',
        '__cpp_constexpr',
        '__cpp_constexpr_in_decltype',
        '__cpp_range_based_for',
        '__cpp_static_assert',
        '__cpp_decltype',
        '__cpp_attributes',
        '__cpp_rvalue_references',
        '__cpp_variadic_templates',
        '__cpp_initializer_lists',
        '__cpp_delegating_constructors',
        '__cpp_nsdmi',
        '__cpp_inheriting_constructors',
        '__cpp_ref_qualifiers',
        '__cpp_alias_templates',
        '__cpp_threadsafe_static_init',
        '__cpp_binary_literals',
        '__cpp_digit_separators',
        '__cpp_init_captures',
        '__cpp_generic_lambdas',
        '__cpp_decltype_auto',
        '__cpp_return_type_deduction',
        '__cpp_aggregate_nsdmi',
        '__cpp_variable_templates',
        '__cpp_impl_destroying_delete',
    )

    if domain not in ['c', 'cpp']:
        errors.append(ParserError(ErrorLevel.CRITICAL, None, None,
                                  f'domain \'{domain}\' not in [\'c\', \'cpp\']'))
        return False

    for cursor in tu.cursor.get_children():
        if cursor.kind == CursorKind.MACRO_DEFINITION and cursor.spelling in cpp_macros:
            if domain != 'cpp':
                errors.append(ParserError(ErrorLevel.CRITICAL, None, None,
                                          f'domain ({domain}) does not match inferred domain (cpp)'))  # noqa: E501
                return False
            return True

    if domain != 'c':
        errors.append(ParserError(ErrorLevel.CRITICAL, None, None,
                                  f'domain ({domain}) does not match inferred domain (c)'))  # noqa: E501
        return False
    return True

def _comment_extract(tu):

    # FIXME: How to handle top level comments above a cursor that it does *not*
    # describe? Parsing @file or @doc at this stage would not be a clean design.
    # One idea is to use '/***' to denote them, but that might throw off editor
    # highlighting. The workaround is to follow the top level comment with an
    # empty '/**/' comment that gets attached to the cursor.

    top_level_comments = []
    comments = {}
    current_comment = None

    is_doc = lambda cursor: cursor and docstring.Docstring.is_doc(cursor.spelling)

    for token in tu.get_tokens(extent=tu.cursor.extent):
        # Handle all comments we come across.
        if token.kind == TokenKind.COMMENT:
            # If we already have a comment, it wasn't related to another cursor.
            if is_doc(current_comment):
                top_level_comments.append(current_comment)
            current_comment = token
            continue

        # Store off the token's cursor for a slight performance improvement
        # instead of accessing the `cursor` property multiple times.
        token_cursor = token.cursor

        # Cursors that are 1) never documented themselves, and 2) allowed
        # between the comment and the actual cursor being documented.
        if token_cursor.kind in [CursorKind.INVALID_FILE,
                                 CursorKind.TYPE_REF,
                                 CursorKind.TEMPLATE_REF,
                                 CursorKind.NAMESPACE_REF,
                                 CursorKind.PREPROCESSING_DIRECTIVE,
                                 CursorKind.MACRO_INSTANTIATION]:
            continue

        # Cursors that are 1) never documented themselves, and 2) not allowed
        # between the comment and the actual cursor being documented.
        if token_cursor.kind in [CursorKind.UNEXPOSED_DECL]:
            if is_doc(current_comment):
                top_level_comments.append(current_comment)
            current_comment = None
            continue

        # Otherwise the current comment documents _this_ cursor. I.e.: not a top
        # level comment.
        if is_doc(current_comment):
            comments[token_cursor.hash] = current_comment
        current_comment = None

    # Comment at the end of file.
    if is_doc(current_comment):
        top_level_comments.append(current_comment)

    return top_level_comments, comments

def _recursive_parse(domain, comments, errors, cursor, nest):
    comment = comments[cursor.hash]
    name = cursor.spelling
    ttype = cursor.type.spelling
    text = comment.spelling
    meta = _get_meta(comment, cursor)

    if cursor.kind == CursorKind.MACRO_DEFINITION:
        cc = MacroDefinition(domain, cursor, comment)

        args = cc.get_args()

        if args is None:
            ds = docstring.MacroDocstring(domain=domain, text=text,
                                          nest=nest, name=name, meta=meta)
        else:
            ds = docstring.MacroFunctionDocstring(domain=domain, text=text,
                                                  nest=nest, name=name,
                                                  args=args, meta=meta)

        return [ds]

    elif cursor.kind in [CursorKind.VAR_DECL, CursorKind.FIELD_DECL]:
        cc = VarFieldDecl(domain, cursor, comment)

        # Note: Preserve original name
        ttype, decl_name = cc.var_type_fixup()

        if cursor.kind == CursorKind.VAR_DECL:
            ds = docstring.VarDocstring(domain=domain, text=text, nest=nest,
                                        name=name, decl_name=decl_name,
                                        ttype=ttype, meta=meta)
        else:
            ds = docstring.MemberDocstring(domain=domain, text=text, nest=nest,
                                           name=name, decl_name=decl_name,
                                           ttype=ttype, meta=meta)

        return [ds]

    elif cursor.kind == CursorKind.TYPEDEF_DECL:
        # FIXME: function pointers typedefs.
        cc = TypedefDecl(domain, cursor, comment)

        ds = docstring.TypeDocstring(domain=domain, text=text,
                                     nest=nest, name=ttype, meta=meta)

        return [ds]

    elif cursor.kind in [CursorKind.STRUCT_DECL,
                         CursorKind.UNION_DECL,
                         CursorKind.ENUM_DECL,
                         CursorKind.CLASS_DECL,
                         CursorKind.CLASS_TEMPLATE]:
        cc = CompoundDecl(domain, cursor, comment)

        decl_name = cc.type_definition_fixup()

        if cursor.kind == CursorKind.STRUCT_DECL:
            ds = docstring.StructDocstring(domain=domain, text=text,
                                           nest=nest, name=name,
                                           decl_name=decl_name, meta=meta)
        elif cursor.kind == CursorKind.UNION_DECL:
            ds = docstring.UnionDocstring(domain=domain, text=text,
                                          nest=nest, name=name,
                                          decl_name=decl_name, meta=meta)
        elif cursor.kind == CursorKind.ENUM_DECL:
            if cursor.is_scoped_enum():
                ds = docstring.EnumClassDocstring(domain=domain, text=text,
                                                  nest=nest, name=name,
                                                  decl_name=decl_name, meta=meta)
            else:
                ds = docstring.EnumDocstring(domain=domain, text=text,
                                             nest=nest, name=name,
                                             decl_name=decl_name, meta=meta)
        elif cursor.kind in [CursorKind.CLASS_DECL, CursorKind.CLASS_TEMPLATE]:
            ds = docstring.ClassDocstring(domain=domain, text=text,
                                          nest=nest, name=name,
                                          decl_name=decl_name, meta=meta)

        for c in cursor.get_children():
            if c.hash in comments:
                ds.add_children(_recursive_parse(domain, comments,
                                                 errors, c, nest + 1))

        return [ds]

    elif cursor.kind == CursorKind.ENUM_CONSTANT_DECL:
        cc = EnumConstantDecl(domain, cursor, comment)

        value = cc.get_value()

        ds = docstring.EnumeratorDocstring(domain=domain, name=name,
                                           value=value, text=text,
                                           meta=meta, nest=nest)

        return [ds]

    elif cursor.kind == CursorKind.FUNCTION_DECL:
        cc = FunctionDecl(domain, cursor, comment)

        ttype, args = cc.function_fixup()

        ds = docstring.FunctionDocstring(domain=domain, text=text,
                                         nest=nest, name=name,
                                         ttype=ttype, args=args,
                                         quals='', meta=meta)
        return [ds]

    elif cursor.kind in [CursorKind.CONSTRUCTOR,
                         CursorKind.DESTRUCTOR,
                         CursorKind.CXX_METHOD,
                         CursorKind.FUNCTION_TEMPLATE]:
        cc = MethodDecl(domain, cursor, comment)

        ttype, args, quals = cc.method_fixup()

        ds = docstring.FunctionDocstring(domain=domain, text=text,
                                         nest=nest, name=name,
                                         ttype=ttype, args=args,
                                         quals=quals, meta=meta)
        return [ds]

    # If we reach here, nothing matched i.e. there's a documentation comment
    # above an unexpected cursor.
    message = f'documentation comment attached to unexpected cursor {str(cursor.kind)} {cursor.spelling}'  # noqa: E501
    errors.append(ParserError(ErrorLevel.WARNING, cursor.location.file.name,
                              cursor.location.line, message))

    cc = TopLevelComment(comment=comment)
    ds = docstring.TextDocstring(text=text, meta=meta)

    return [ds]

def _clang_diagnostics(diagnostics, errors):
    for diag in diagnostics:
        filename = diag.location.file.name if diag.location.file else None
        errors.append(ParserError(ErrorLevel(diag.severity), filename,
                                  diag.location.line, diag.spelling))

def _parse_undocumented_block(domain, comments, errors, cursor, nest):
    """Parse undocumented blocks.

    Some blocks define plenty of children that may be documented themselves
    while the parent cursor itself has no documentation. One such example is the
    `extern "C"` block.
    """
    ret = []

    # Identify `extern "C"` and `extern "C++"` blocks and recursively parse
    # their contents. Only `extern "C"` is of any relevance in choosing a
    # different domain.
    # For some reason, the Python bindings don't return the cursor kind
    # LINKAGE_SPEC as one would expect, so we need to do it the hard way.
    if cursor.kind == CursorKind.UNEXPOSED_DECL:
        tokens = _cursor_get_tokens(cursor)
        ntoken = next(tokens, None)
        if ntoken and ntoken.spelling == 'extern':
            ntoken = next(tokens, None)

            if not ntoken:
                return ret

            if ntoken.spelling == '"C"':
                domain = 'c'
            elif ntoken.spelling == '"C++"':
                domain = 'cpp'
            else:
                message = f'unhandled `extern {ntoken.spelling}` block will mask all children'
                errors.append(ParserError(ErrorLevel.WARNING,
                                          cursor.location.file.name,
                                          cursor.location.line, message))
                return ret

            for c in cursor.get_children():
                if c.hash in comments:
                    ret.extend(_recursive_parse(domain, comments, errors, c, nest))

    return ret

# Parse a file and return a tree of docstring.Docstring objects.
def parse(filename, domain=None, clang_args=None):
    # Empty root comment with just children
    result = docstring.RootDocstring(filename=filename, domain=domain,
                                     clang_args=clang_args)
    errors = []
    index = Index.create()

    try:
        tu = index.parse(filename, args=clang_args,
                         options=TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD |
                         TranslationUnit.PARSE_SKIP_FUNCTION_BODIES)
    except TranslationUnitLoadError as e:
        # File not found is a common problem, but not properly reported by
        # clang. Try to be a bit more helpful.
        if not os.path.isfile(filename):
            message = f'File not found. {str(e)}'
        else:
            message = str(e)

        errors.append(ParserError(ErrorLevel.CRITICAL, filename, None, message))

        return result, errors

    _clang_diagnostics(tu.diagnostics, errors)

    if not _domain_is_valid(tu, domain, errors):
        return result, errors

    top_level_comments, comments = _comment_extract(tu)

    for comment in top_level_comments:
        cc = TopLevelComment(comment=comment)

        text = comment.spelling
        meta = _get_meta(comment)
        ds = docstring.TextDocstring(text=text, meta=meta)
        result.add_child(ds)

    for cursor in tu.cursor.get_children():
        if cursor.hash in comments:
            result.add_children(_recursive_parse(domain, comments,
                                                 errors, cursor, 0))
        else:
            result.add_children(_parse_undocumented_block(domain, comments,
                                                          errors, cursor, 0))

    return result, errors
