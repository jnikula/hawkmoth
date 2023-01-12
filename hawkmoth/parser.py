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
from dataclasses import dataclass

from clang.cindex import TokenKind, CursorKind, TypeKind, StorageClass
from clang.cindex import Index, TranslationUnit
from clang.cindex import Diagnostic

from hawkmoth import docstring

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
            return f'{self.filename}:{self.line}: {self.message}'
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

def _get_meta(comment, cursor=None):
    meta = {'line': comment.extent.start.line}
    if cursor:
        meta['cursor.kind'] = cursor.kind
        meta['cursor.displayname'] = cursor.displayname
        meta['cursor.spelling'] = cursor.spelling

    return meta

# Return None for simple macros, a potentially empty list of arguments for
# function-like macros
def _get_macro_args(cursor):
    if cursor.kind != CursorKind.MACRO_DEFINITION:
        return None

    tokens = cursor.get_tokens()

    # Use the first two tokens to make sure this starts with 'IDENTIFIER('
    one = next(tokens)
    two = next(tokens, None)
    if two is None or one.extent.end != two.extent.start or two.spelling != '(':
        return None

    # Naïve parsing of macro arguments
    # FIXME: This doesn't handle GCC named vararg extension FOO(vararg...)
    args = []
    for token in tokens:
        if token.spelling == ')':
            return args
        elif token.spelling == ',':
            continue
        elif token.kind == TokenKind.IDENTIFIER:
            args.extend([('', token.spelling)])
        elif token.spelling == '...':
            args.extend([('', token.spelling)])
        else:
            break

    return None

def _get_storage_class(cursor):
    """Get the storage class of a cursor.

    Only storage classes that are relevant to the documentation are returned.

    Returns:
        Storage class as a string. ``None`` otherwise.
    """
    storage_class_map = {
        StorageClass.EXTERN: 'extern',
        StorageClass.STATIC: 'static',
    }

    return storage_class_map.get(cursor.storage_class)

def _type_fixup(cursor):
    """Fix non trivial types' spelling and append qualifiers.

    If this is an array, the dimensions should be applied to the name, not
    the type.
    If this is a function pointer, or an array of function pointers, the
    name should be within the parenthesis as in ``(*name)`` or ``(*name[N])``.
    """
    cursor_type = cursor.type

    stars_and_quals = ''
    dims = ''
    while True:
        if cursor_type.kind == TypeKind.POINTER:
            quals = []
            if cursor_type.is_const_qualified():
                quals.append('const')
            if cursor_type.is_volatile_qualified():
                quals.append('volatile')
            if cursor_type.is_restrict_qualified():
                quals.append('restrict')

            spacer = ' ' if quals and stars_and_quals else ''
            stars_and_quals = '*' + ' '.join(quals) + spacer + stars_and_quals

            cursor_type = cursor_type.get_pointee()
        elif cursor_type.kind == TypeKind.CONSTANTARRAY:
            dims += f'[{cursor_type.element_count}]'
            cursor_type = cursor_type.get_array_element_type()
        elif cursor_type.kind == TypeKind.INCOMPLETEARRAY:
            dims += '[]'
            cursor_type = cursor_type.get_array_element_type()
        else:
            break

    if cursor_type.kind == TypeKind.FUNCTIONPROTO:
        pad = lambda s: s if s.endswith('*') else s + ' '

        args = []
        for c in cursor.get_children():
            if c.kind == CursorKind.PARM_DECL:
                arg_ttype, arg_name = _type_fixup(c)
                args.append(f'{pad(arg_ttype)}{arg_name}' if arg_name else arg_ttype)
        if cursor_type.is_function_variadic():
            args.append('...')
        if len(args) == 0:
            args.append('void')

        ret_type = cursor_type.get_result().spelling

        ttype = ''
        name = f'''{pad(ret_type)}({pad(stars_and_quals)}{cursor.spelling}{dims})({', '.join(args)})'''  # noqa: E501
    else:
        type_elem = []

        storage_class = _get_storage_class(cursor)
        if storage_class:
            type_elem.append(storage_class)

        type_elem.append(cursor_type.spelling)

        if stars_and_quals:
            type_elem.append(stars_and_quals)

        ttype = ' '.join(type_elem)
        name = cursor.spelling + dims

    return ttype, name

def _get_args(cursor):
    """Get function / method arguments."""
    args = []

    # Only fully prototyped functions will have argument lists to process.
    if cursor.type.kind == TypeKind.FUNCTIONPROTO:
        for c in cursor.get_children():
            if c.kind == CursorKind.PARM_DECL:
                arg_ttype, arg_name = _type_fixup(c)
                args.extend([(arg_ttype, arg_name)])

        if cursor.type.is_function_variadic():
            args.extend([('', '...')])
        if len(args) == 0:
            args.extend([('', 'void')])

    return args

def _recursive_parse(domain, comments, errors, cursor, nest):
    comment = comments[cursor.hash]
    name = cursor.spelling
    ttype = cursor.type.spelling
    text = comment.spelling
    meta = _get_meta(comment, cursor)

    if cursor.kind == CursorKind.MACRO_DEFINITION:
        # FIXME: check args against comment
        args = _get_macro_args(cursor)

        if args is None:
            ds = docstring.MacroDocstring(domain=domain, text=text,
                                          nest=nest, name=name, meta=meta)
        else:
            ds = docstring.MacroFunctionDocstring(domain=domain, text=text,
                                                  nest=nest, name=name,
                                                  args=args, meta=meta)

        return [ds]

    elif cursor.kind in [CursorKind.VAR_DECL, CursorKind.FIELD_DECL]:
        # Note: Preserve original name
        ttype, decl_name = _type_fixup(cursor)

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

        ds = docstring.TypeDocstring(domain=domain, text=text,
                                     nest=nest, name=ttype, meta=meta)

        return [ds]

    elif cursor.kind in [CursorKind.STRUCT_DECL, CursorKind.UNION_DECL,
                         CursorKind.ENUM_DECL]:

        # Do not set the decl_name for anonymous symbols (empty spelling).
        decl_name = name if cursor.spelling != '' else None

        if cursor.kind == CursorKind.STRUCT_DECL:
            ds = docstring.StructDocstring(domain=domain, text=text,
                                           nest=nest, name=name,
                                           decl_name=decl_name, meta=meta)
        elif cursor.kind == CursorKind.UNION_DECL:
            ds = docstring.UnionDocstring(domain=domain, text=text,
                                          nest=nest, name=name,
                                          decl_name=decl_name, meta=meta)
        else:
            ds = docstring.EnumDocstring(domain=domain, text=text,
                                         nest=nest, name=name,
                                         decl_name=decl_name, meta=meta)

        for c in cursor.get_children():
            if c.hash in comments:
                ds.add_children(_recursive_parse(domain, comments,
                                                 errors, c, nest + 1))

        return [ds]

    elif cursor.kind == CursorKind.ENUM_CONSTANT_DECL:
        ds = docstring.EnumeratorDocstring(domain=domain, text=text,
                                           nest=nest, name=name, meta=meta)

        return [ds]

    elif cursor.kind == CursorKind.FUNCTION_DECL:
        args = _get_args(cursor)
        ttype = cursor.result_type.spelling

        ds = docstring.FunctionDocstring(domain=domain, text=text,
                                         nest=nest, name=name,
                                         ttype=ttype, args=args, meta=meta)
        return [ds]

    # If we reach here, nothing matched i.e. there's a documentation comment
    # above an unexpected cursor.
    message = f'documentation comment attached to unexpected cursor {str(cursor.kind)} {cursor.spelling}'  # noqa: E501
    errors.append(ParserError(ErrorLevel.WARNING, cursor.location.file.name,
                              cursor.location.line, message))

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
        tokens = cursor.get_tokens()
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
    errors = []
    index = Index.create()

    tu = index.parse(filename, args=clang_args,
                     options=TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD |
                     TranslationUnit.PARSE_SKIP_FUNCTION_BODIES)

    _clang_diagnostics(tu.diagnostics, errors)

    if not _domain_is_valid(tu, domain, errors):
        return docstring.Docstring(), errors

    top_level_comments, comments = _comment_extract(tu)

    # Empty comment with just children
    result = docstring.Docstring()

    for comment in top_level_comments:
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
