# Copyright (c) 2016-2017 Jani Nikula <jani@nikula.org>
# Copyright (c) 2018-2020 Bruno Santos <brunomanuelsantos@tecnico.ulisboa.pt>
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
import re

from clang.cindex import TokenKind, CursorKind, TypeKind
from clang.cindex import Index, TranslationUnit

from hawkmoth import docstring

class ErrorLevel(enum.Enum):
    """
    Supported error levels in inverse numerical order of severity. The values
    are chosen so that they map directly to a 'verbosity level'.
    """
    ERROR = 0
    WARNING = 1
    INFO = 2
    DEBUG = 3

def _comment_extract(tu):

    # FIXME: How to handle top level comments above a cursor that it does *not*
    # describe? Parsing @file or @doc at this stage would not be a clean design.
    # One idea is to use '/***' to denote them, but that might throw off editor
    # highlighting. The workaround is to follow the top level comment with an
    # empty '/**/' comment that gets attached to the cursor.

    top_level_comments = []
    comments = {}
    cursor = None
    current_comment = None
    for token in tu.get_tokens(extent=tu.cursor.extent):
        # handle all comments we come across
        if token.kind == TokenKind.COMMENT:
            # if we already have a comment, it wasn't related to a cursor
            if current_comment and docstring.Docstring.is_doc(current_comment.spelling):
                top_level_comments.append(current_comment)
            current_comment = token
            continue

        # Store off the token's cursor for a slight performance improvement
        # instead of accessing the `cursor` property multiple times.
        token_cursor = token.cursor

        # cursors that are 1) never documented themselves, and 2) allowed
        # between comment and the actual cursor being documented
        if token_cursor.kind in [CursorKind.INVALID_FILE,
                                 CursorKind.TYPE_REF,
                                 CursorKind.PREPROCESSING_DIRECTIVE,
                                 CursorKind.MACRO_INSTANTIATION]:
            continue

        if cursor is not None and token_cursor == cursor:
            continue

        cursor = token_cursor

        # Note: current_comment may be None
        if current_comment is not None and docstring.Docstring.is_doc(current_comment.spelling):
            comments[cursor.hash] = current_comment
        current_comment = None

    # comment at the end of file
    if current_comment and docstring.Docstring.is_doc(current_comment.spelling):
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
            args.append(token.spelling)
        elif token.spelling == '...':
            args.append(token.spelling)
        else:
            break

    return None

# If this is an array, the dimensions should be applied to the name, not
# the type.
def _array_fixup(ttype, name):
    dims = ttype.rsplit(' ', 1)[-1]
    if dims.startswith('[') and dims.endswith(']'):
        ttype = ttype.rsplit(' ', 1)[0]
        name = name + dims

    return ttype, name

# If this is a function pointer, or an array of function pointers, the
# name should be within the parenthesis as in (*name) or (*name[N]).
def _function_pointer_fixup(ttype, name):
    mo = re.match(r'(?P<begin>.+)\((?P<stars>\*+)(?P<qual>[a-zA-Z_ ]+)?(?P<brackets>\[[^]]*\])?\)(?P<end>.+)', ttype)  # noqa: E501
    if mo is None:
        return ttype, name

    begin = mo.group('begin')
    stars = mo.group('stars')
    qual = mo.group('qual') + ' ' if mo.group('qual') is not None else ''
    brackets = mo.group('brackets') if mo.group('brackets') is not None else ''
    end = mo.group('end')

    name = f'{begin}({stars}{qual}{name}{brackets}){end}'
    ttype = ''

    return ttype, name

def _decl_fixup(ttype, name):
    ttype, name = _array_fixup(ttype, name)

    ttype, name = _function_pointer_fixup(ttype, name)

    return ttype, name

# name may be empty for typedefs and anonymous enums, structs and unions
def _anonymous_fixup(ttype, name):
    if name:
        return ttype, name

    mo = re.match(r'(?a)^(?P<type>enum|struct|union) ([^:]+::)?\(anonymous at [^)]+\)$', ttype)
    if mo:
        # Anonymous
        name = ''
    else:
        # Typedef
        name = ttype

    return ttype, name

def _recursive_parse(comments, cursor, nest):
    comment = comments[cursor.hash]
    name = cursor.spelling
    ttype = cursor.type.spelling
    text = comment.spelling
    meta = _get_meta(comment, cursor)

    if cursor.kind == CursorKind.MACRO_DEFINITION:
        # FIXME: check args against comment
        args = _get_macro_args(cursor)

        if args is None:
            ds = docstring.MacroDocstring(text=text, nest=nest, name=name, meta=meta)
        else:
            ds = docstring.MacroFunctionDocstring(text=text, nest=nest,
                                                  name=name, args=args, meta=meta)

        return [ds]

    elif cursor.kind in [CursorKind.VAR_DECL, CursorKind.FIELD_DECL]:
        # Note: Preserve original name
        ttype, decl_name = _decl_fixup(ttype, name)

        if cursor.kind == CursorKind.VAR_DECL:
            ds = docstring.VarDocstring(text=text, nest=nest, name=name,
                                        decl_name=decl_name, ttype=ttype, meta=meta)
        else:
            ds = docstring.MemberDocstring(text=text, nest=nest, name=name,
                                           decl_name=decl_name, ttype=ttype, meta=meta)

        return [ds]

    elif cursor.kind == CursorKind.TYPEDEF_DECL:
        # FIXME: function pointers typedefs.

        ds = docstring.TypeDocstring(text=text, nest=nest, name=ttype, meta=meta)

        return [ds]

    elif cursor.kind in [CursorKind.STRUCT_DECL, CursorKind.UNION_DECL,
                         CursorKind.ENUM_DECL]:

        # FIXME:
        # Handle cases where variables are instantiated on type declaration,
        # including anonymous cases. Idea is that if there is a variable
        # instantiation, the documentation should be applied to the variable if
        # the structure is anonymous or to the type otherwise.
        #
        # Due to the new recursiveness of the parser, fixing this here, _should_
        # handle all cases (struct, union, enum).

        # Note: Preserve original name
        ttype, decl_name = _anonymous_fixup(ttype, name)

        if cursor.kind == CursorKind.STRUCT_DECL:
            ds = docstring.StructDocstring(text=text, nest=nest, name=name,
                                           decl_name=decl_name, meta=meta)
        elif cursor.kind == CursorKind.UNION_DECL:
            ds = docstring.UnionDocstring(text=text, nest=nest, name=name,
                                          decl_name=decl_name, meta=meta)
        else:
            ds = docstring.EnumDocstring(text=text, nest=nest, name=name,
                                         decl_name=decl_name, meta=meta)

        for c in cursor.get_children():
            if c.hash in comments:
                ds.add_children(_recursive_parse(comments, c, nest + 1))

        return [ds]

    elif cursor.kind == CursorKind.ENUM_CONSTANT_DECL:
        ds = docstring.EnumeratorDocstring(text=text, nest=nest, name=name, meta=meta)

        return [ds]

    elif cursor.kind == CursorKind.FUNCTION_DECL:
        # FIXME: check args against comment
        # FIXME: children may contain extra stuff if the return type is a
        # typedef, for example
        args = []

        # Only fully prototyped functions will have argument lists to process.
        if cursor.type.kind == TypeKind.FUNCTIONPROTO:
            for c in cursor.get_children():
                if c.kind == CursorKind.PARM_DECL:
                    arg_ttype, arg_name = _decl_fixup(c.type.spelling, c.spelling)

                    args.append(f'{arg_ttype} {arg_name}')

            if cursor.type.is_function_variadic():
                args.append('...')

        ttype = cursor.result_type.spelling

        ds = docstring.FunctionDocstring(text=text, nest=nest, name=name,
                                         ttype=ttype, args=args, meta=meta)
        return [ds]

    # FIXME: If we reach here, nothing matched. This is a warning or even error
    # and it should be logged, but it should also return an empty list so that
    # it doesn't break. I.e. the parser needs to pass warnings and errors to the
    # Sphinx extension instead of polluting the generated output.
    kind = str(cursor.kind)
    text = f'warning: unhandled cursor {kind} {cursor.spelling}\n'
    meta = _get_meta(comment, cursor)

    ds = docstring.TextDocstring(text=text, meta=meta)

    return [ds]

def _clang_diagnostics(diagnostics):
    errors = []
    sev = {0: ErrorLevel.DEBUG,
           1: ErrorLevel.DEBUG,
           2: ErrorLevel.WARNING,
           3: ErrorLevel.ERROR,
           4: ErrorLevel.ERROR}

    for diag in diagnostics:
        filename = diag.location.file.name if diag.location.file else None
        errors.extend([(sev[diag.severity], filename,
                        diag.location.line, diag.spelling)])

    return errors

# Parse a file and return a tree of docstring.Docstring objects.
def parse(filename, clang_args=None):
    index = Index.create()

    tu = index.parse(filename, args=clang_args,
                     options=TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD |
                     TranslationUnit.PARSE_SKIP_FUNCTION_BODIES)

    errors = _clang_diagnostics(tu.diagnostics)

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
            result.add_children(_recursive_parse(comments, cursor, 0))

    return result, errors
