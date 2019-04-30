# Copyright (c) 2016-2017 Jani Nikula <jani@nikula.org>
# Copyright (c) 2018-2019 Bruno Santos <brunomanuelsantos@tecnico.ulisboa.pt>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.
"""
Documentation comment extractor
===============================

This module extracts relevant documentation comments, optionally reformatting
them in reST syntax.

This is the part that uses Clang Python Bindings to extract documentation
comments from C source code. This module does not depend on Sphinx.

There are two passes:

#. Pass over the tokens to find all the comments, including ones that aren't
   attached to cursors.

#. Pass over the cursors to document them.

There is minimal syntax parsing or input conversion:

* Identification of documentation comment blocks, and stripping the comment
  delimiters (``/**`` and ``*/``) and continuation line prefixes (e.g. ``␣*␣``).

* Identification of function-like macros.

* Indentation for reST C Domain directive blocks.

* An optional external filter may be invoked to support different syntaxes.
  These filters are expected to translate the comment into the reST format.

Otherwise, documentation comments are passed through verbatim.
"""

import enum
import itertools
import sys

from clang.cindex import CursorKind
from clang.cindex import Index, TranslationUnit
from clang.cindex import SourceLocation, SourceRange
from clang.cindex import TokenKind, TokenGroup

from hawkmoth.util import docstr, doccompat

class ErrorLevel(enum.Enum):
    """
    Supported error levels in inverse numerical order of severity. The values
    are chosen so that they map directly to a 'verbosity level'.
    """
    ERROR = 0
    WARNING = 1
    INFO = 2
    DEBUG = 3

def comment_extract(tu):

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
            if current_comment and docstr.is_doc(current_comment.spelling):
                top_level_comments.append(current_comment)
            current_comment = token
            continue

        # cursors that are 1) never documented themselves, and 2) allowed
        # between comment and the actual cursor being documented
        if (token.cursor.kind == CursorKind.INVALID_FILE or
            token.cursor.kind == CursorKind.TYPE_REF or
            token.cursor.kind == CursorKind.PREPROCESSING_DIRECTIVE or
            token.cursor.kind == CursorKind.MACRO_INSTANTIATION):
            continue

        if cursor is not None and token.cursor == cursor:
            continue

        cursor = token.cursor

        # Note: current_comment may be None
        if current_comment != None and docstr.is_doc(current_comment.spelling):
            comments[cursor.hash] = current_comment
        current_comment = None

    # comment at the end of file
    if current_comment and docstr.is_doc(current_comment.spelling):
        top_level_comments.append(current_comment)

    return top_level_comments, comments

def _result(comment, cursor=None, fmt=docstr.Type.TEXT, nest=0,
            name=None, ttype=None, args=None, compat=None):

    # FIXME: docstr.generate changes the number of lines in output. This impacts
    # the error reporting via meta['line']. Adjust meta to take this into
    # account.

    doc = docstr.generate(text=comment.spelling, fmt=fmt,
                          name=name, ttype=ttype, args=args, transform=compat)

    doc = docstr.nest(doc, nest)

    meta = {'line': comment.extent.start.line}
    if cursor:
        meta['cursor.kind']        = cursor.kind,
        meta['cursor.displayname'] = cursor.displayname,
        meta['cursor.spelling']    = cursor.spelling

    return [(doc, meta)]

# Return None for simple macros, a potentially empty list of arguments for
# function-like macros
def _get_macro_args(cursor):
    if cursor.kind != CursorKind.MACRO_DEFINITION:
        return None

    # Use the first two tokens to make sure this starts with 'IDENTIFIER('
    x = [token for token in itertools.islice(cursor.get_tokens(), 2)]
    if (len(x) != 2 or x[0].spelling != cursor.spelling or
        x[1].spelling != '(' or x[0].extent.end != x[1].extent.start):
        return None

    # Naïve parsing of macro arguments
    # FIXME: This doesn't handle GCC named vararg extension FOO(vararg...)
    args = []
    for token in itertools.islice(cursor.get_tokens(), 2, None):
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

def _recursive_parse(comments, cursor, nest, compat):
    comment = comments[cursor.hash]
    name = cursor.spelling
    ttype = cursor.type.spelling

    if cursor.kind == CursorKind.MACRO_DEFINITION:
        # FIXME: check args against comment
        args = _get_macro_args(cursor)
        fmt = docstr.Type.MACRO if args is None else docstr.Type.MACRO_FUNC

        return _result(comment, cursor=cursor, fmt=fmt,
                       nest=nest, name=name, args=args, compat=compat)

    elif cursor.kind == CursorKind.VAR_DECL:
        fmt = docstr.Type.VAR

        return _result(comment, cursor=cursor, fmt=fmt,
                       nest=nest, name=name, ttype=ttype, compat=compat)

    elif cursor.kind == CursorKind.TYPEDEF_DECL:
        # FIXME: function pointers typedefs.
        fmt = docstr.Type.TYPE

        return _result(comment, cursor=cursor, fmt=fmt,
                       nest=nest, name=ttype, compat=compat)

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

        # FIXME: Handle anonymous enumerators.

        fmt = docstr.Type.TYPE
        result = _result(comment, cursor=cursor, fmt=fmt,
                         nest=nest, name=ttype, compat=compat)

        nest += 1
        for c in cursor.get_children():
            if c.hash in comments:
                result.extend(_recursive_parse(comments, c, nest, compat))

        return result

    elif cursor.kind == CursorKind.ENUM_CONSTANT_DECL:
        fmt = docstr.Type.ENUM_VAL

        return _result(comment, cursor=cursor, fmt=fmt,
                       nest=nest, name=name, compat=compat)

    elif cursor.kind == CursorKind.FIELD_DECL:
        fmt = docstr.Type.MEMBER

        return _result(comment, cursor=cursor, fmt=fmt,
                       nest=nest, name=name, ttype=ttype, compat=compat)

    elif cursor.kind == CursorKind.FUNCTION_DECL:
        # FIXME: check args against comment
        # FIXME: children may contain extra stuff if the return type is a
        # typedef, for example
        args = []
        for c in cursor.get_children():
            if c.kind == CursorKind.PARM_DECL:
                args.append('{ttype} {arg}'.format(ttype=c.type.spelling,
                                                   arg=c.spelling))

        if cursor.type.is_function_variadic():
            args.append('...')

        fmt = docstr.Type.FUNC
        ttype = cursor.result_type.spelling

        return _result(comment, cursor=cursor, fmt=fmt, nest=nest,
                       name=name, ttype=ttype, args=args, compat=compat)

    # FIXME: If we reach here, nothing matched. This is a warning or even error
    # and it should be logged, but it should also return an empty list so that
    # it doesn't break. I.e. the parser needs to pass warnings and errors to the
    # Sphinx extension instead of polluting the generated output.
    fmt = docstr.Type.TEXT
    text = 'warning: unhandled cursor {kind} {name}\n'.format(
        kind=str(cursor.kind),
        name=cursor.spelling)

    doc = docstr.generate(text=text, fmt=fmt)

    meta = {
        'line':               comment.extent.start.line,
        'cursor.kind':        cursor.kind,
        'cursor.displayname': cursor.displayname,
        'cursor.spelling':    cursor.spelling
    }

    return [(doc, meta)]

def clang_diagnostics(errors, diagnostics):
    sev = {0: ErrorLevel.DEBUG,
           1: ErrorLevel.DEBUG,
           2: ErrorLevel.WARNING,
           3: ErrorLevel.ERROR,
           4: ErrorLevel.ERROR}

    for diag in diagnostics:
        errors.extend([(sev[diag.severity], diag.location.file.name,
                        diag.location.line, diag.spelling)])

# return a list of (comment, metadata) tuples
# options - dictionary with directive options
def parse(filename, **options):

    errors = []
    args = options.get('clang')
    if args is not None:
        args = [s.strip() for s in args.split(',') if len(s.strip()) > 0]
        if len(args) == 0:
            args = None

    index = Index.create()

    tu = index.parse(filename, args=args, options=
                     TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD |
                     TranslationUnit.PARSE_SKIP_FUNCTION_BODIES)

    clang_diagnostics(errors, tu.diagnostics)

    top_level_comments, comments = comment_extract(tu)

    result = []
    compat = lambda x: doccompat.convert(x, options.get('compat'))

    for comment in top_level_comments:
        result.extend(_result(comment, compat=compat))

    for cursor in tu.cursor.get_children():
        if cursor.hash in comments:
            result.extend(_recursive_parse(comments, cursor, 0, compat))

    # Sort all elements by order of appearance.
    result.sort(key=lambda r: r[1]['line'])

    return result, errors
