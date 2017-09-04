#!/usr/bin/env python
# coding=utf-8
"""Hawkmoth - Documentation comment extractor based on Clang"""

__author__ = "Jani Nikula <jani@nikula.org>"
__copyright__ = "Copyright (c) 2016-2017, Jani Nikula <jani@nikula.org>"
__version__  = '0.1'
__license__ = "BSD 2-Clause, see LICENSE for details"

import argparse
import itertools
import re
import sys

from clang.cindex import CursorKind
from clang.cindex import Index, TranslationUnit
from clang.cindex import SourceLocation, SourceRange
from clang.cindex import TokenKind, TokenGroup

# This is the part that uses Clang Python Bindings to extract documentation
# comments from C source code.
#
# Do not depend on Sphinx here.
#
# We have to do two passes. First pass over the tokens to find all the comments,
# including ones that aren't attached to cursors. Second pass over the cursors
# to document them.
#
# There is minimal syntax parsing or input conversion:
#
#   - Identification of documentation comment blocks, and stripping the comment
#     delimiters ("/**" and "*/") and continuation line prefixes (e.g. " * ").
#
#   - Identification of function-like macros.
#
#   - Indentation for reStructuredText C Domain directive blocks.
#
#   - Optional conversion of the simplest Javadoc tags to native
#     reStructuredText field lists.
#
# Otherwise, pass through the documentation comments verbatim.

def is_doc_comment(comment):
    return comment.startswith('/**') and comment != '/**/'

def strip_comment(comment):
    comment = re.sub(r"^/\*\*[ \t]?", "", comment)
    comment = re.sub(r"\*/$", "", comment)
    # could look at first line of comment, and remove the leading stuff there from the rest
    comment = re.sub(r"(?m)^[ \t]*\*?[ \t]?", "", comment)
    # Strip leading blank lines.
    comment = re.sub(r"^[\n]*", "", comment)
    # End in exactly one newline.
    comment = re.sub(r"[\n]*$", "\n", comment)
    return comment

def indent(string, prefix):
    return re.sub('(?m)^', prefix, string)

def wrap_blank_lines(string):
    return '\n' + string + '\n'

# Basic Javadoc/Doxygen/kernel-doc import
#
# FIXME: One of the design goals of Hawkmoth is to keep things simple. There's a
# fine balance between sticking to that goal and adding compat code to
# facilitate any kind of migration to Hawkmoth. The compat code could be turned
# into a fairly simple plugin architecture, with some basic compat builtins, and
# the users could still extend the compat features to fit their specific needs.
def compat_convert(comment, mode):
    # FIXME: try to preserve whitespace better

    if mode == 'javadoc-basic' or mode == 'javadoc-liberal':
        # @param
        comment = re.sub(r"(?m)^([ \t]*)@param([ \t]+)([a-zA-Z0-9_]+|\.\.\.)([ \t]+)",
                         "\n\\1:param\\2\\3:\\4", comment)
        # @param[direction]
        comment = re.sub(r"(?m)^([ \t]*)@param\[([^]]*)\]([ \t]+)([a-zA-Z0-9_]+|\.\.\.)([ \t]+)",
                         "\n\\1:param\\3\\4: *(\\2)* \\5", comment)
        # @return
        comment = re.sub(r"(?m)^([ \t]*)@returns?([ \t]+|$)",
                         "\n\\1:return:\\2", comment)
        # @code/@endcode blocks. Works if the code is indented.
        comment = re.sub(r"(?m)^([ \t]*)@code([ \t]+|$)",
                         "\n::\n", comment)
        comment = re.sub(r"(?m)^([ \t]*)@endcode([ \t]+|$)",
                         "\n", comment)
        # Ignore @brief.
        comment = re.sub(r"(?m)^([ \t]*)@brief[ \t]+", "\n\\1", comment)

        # Ignore groups
        comment = re.sub(r"(?m)^([ \t]*)@(defgroup|addtogroup)[ \t]+[a-zA-Z0-9_]+[ \t]*",
                         "\n\\1", comment)
        comment = re.sub(r"(?m)^([ \t]*)@(ingroup|{|}).*", "\n", comment)

    if mode == 'javadoc-liberal':
        # Liberal conversion of any @tags, will fail for @code etc. but don't
        # care.
        comment = re.sub(r"(?m)^([ \t]*)@([a-zA-Z0-9_]+)([ \t]+)",
                         "\n\\1:\\2:\\3", comment)

    if mode == 'kernel-doc':
        # Basic kernel-doc convert, will document struct members as params, etc.
        comment = re.sub(r"(?m)^([ \t]*)@(returns?|RETURNS?):([ \t]+|$)",
                         "\n\\1:return:\\3", comment)
        comment = re.sub(r"(?m)^([ \t]*)@([a-zA-Z0-9_]+|\.\.\.):([ \t]+)",
                         "\n\\1:param \\2:\\3", comment)

    return comment

def pass1(tu, top_level_comments, comments):
    cursor = None
    current_comment = None
    for token in tu.get_tokens(extent=tu.cursor.extent):
        # handle all comments we come across
        if token.kind == TokenKind.COMMENT:
            # if we already have a comment, it wasn't related to a cursor
            if current_comment:
                top_level_comments.append(current_comment)
            current_comment = token
            continue

        # cursors that are 1) never documented themselves, and 2) allowed
        # between comment and the actual cursor being documented
        if token.cursor.kind == CursorKind.INVALID_FILE or \
           token.cursor.kind == CursorKind.TYPE_REF or \
           token.cursor.kind == CursorKind.PREPROCESSING_DIRECTIVE or \
           token.cursor.kind == CursorKind.MACRO_INSTANTIATION:
            continue

        if cursor is not None and token.cursor == cursor:
            continue

        cursor = token.cursor

        # Note: current_comment may be None
        if current_comment != None:
            comments[cursor.hash] = current_comment
        current_comment = None

    # comment at the end of file
    if current_comment:
        top_level_comments.append(current_comment)

# Return None for simple macros, a potentially empty list of arguments for
# function-like macros
def get_macro_args(cursor):
    if cursor.kind != CursorKind.MACRO_DEFINITION:
        return None

    # Use the first two tokens to make sure this starts with 'IDENTIFIER('
    x = [token for token in itertools.islice(cursor.get_tokens(), 2)]
    if len(x) != 2 or x[0].spelling != cursor.spelling or \
       x[1].spelling != '(' or x[0].extent.end != x[1].extent.start:
        return None

    # Naïve parsing of macro arguments
    args = []
    for token in itertools.islice(cursor.get_tokens(), 2, None):
        if token.spelling == ')':
            return args
        elif token.spelling == ',':
            continue
        elif token.kind == TokenKind.IDENTIFIER:
            args.append(token.spelling)
        else:
            break

    return None

# return a list of (comment, metadata) tuples
# options - dictionary with directive options
def parse(filename, **options):

    args = options.get('clang')
    if args is not None:
        args = [s.strip() for s in args.split(',') if len(s.strip()) > 0]
        if len(args) == 0:
            args = None

    index = Index.create()

    tu = index.parse(filename, args=args, options=
                     TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD |
                     TranslationUnit.PARSE_SKIP_FUNCTION_BODIES)

    top_level_comments = []
    comments = {}

    # parse the file, get comments
    pass1(tu, top_level_comments, comments)

    # FIXME: strip_comment, compat_convert, and the C Domain directive all
    # change the number of lines in output. This impacts the error reporting via
    # meta['line']. Adjust meta to take this into account.

    result = []

    for comment in top_level_comments:
        if not is_doc_comment(comment.spelling):
            continue

        doc_comment = strip_comment(comment.spelling)
        doc_comment = compat_convert(doc_comment, options.get('compat'))
        doc_comment = wrap_blank_lines(doc_comment)
        meta = { 'line': comment.extent.start.line }

        result.append((doc_comment, meta))

    for cursor in tu.cursor.get_children():
        if cursor.hash not in comments:
            continue
        comment = comments[cursor.hash]
        if not is_doc_comment(comment.spelling):
            continue

        doc_comment = strip_comment(comment.spelling)

        # FIXME: How to handle top level comments above a cursor that it does
        # *not* describe? Parsing @file or @doc at this stage would not be a
        # clean design. One idea is to use '/***' to denote them, but that might
        # throw off editor highlighting. The workaround is to follow the top
        # level comment with an empty '/**/' comment that gets attached to the
        # cursor.

        if cursor.kind == CursorKind.MACRO_DEFINITION:
            args = get_macro_args(cursor)
            if args is None:
                cdom = '.. c:macro:: {name}\n'.format(name=cursor.spelling)
            else:
                # FIXME: check args against doc_comment
                cdom = '.. c:function:: {name}({args})\n'.format(
                    name=cursor.spelling,
                    args=', '.join(args))
        elif cursor.kind == CursorKind.VAR_DECL:
            cdom = '.. c:var:: {type} {name}\n'.format(
                type=cursor.type.spelling,
                name=cursor.spelling)
        elif cursor.kind == CursorKind.TYPEDEF_DECL:
            cdom = '.. c:type:: {name}\n'.format(name=cursor.spelling)
        elif cursor.kind == CursorKind.STRUCT_DECL:
            cdom = '.. c:type:: {name}\n'.format(name=cursor.type.spelling)
        elif cursor.kind == CursorKind.UNION_DECL:
            cdom = '.. c:type:: {name}\n'.format(name=cursor.type.spelling)
        elif cursor.kind == CursorKind.ENUM_DECL:
            cdom = '.. c:type:: {name}\n'.format(name=cursor.type.spelling)
        elif cursor.kind == CursorKind.FUNCTION_DECL:
            # FIXME: check args against doc_comment

            # FIXME: children may contain extra stuff if the return type is a
            # typedef, for example
            # FIXME: handle ... params
            args = []
            for c in cursor.get_children():
                if c.kind == CursorKind.PARM_DECL:
                    args.append('{type} {arg}'.format(
                        type=c.type.spelling,
                        arg=c.spelling))

            cdom = '.. c:function:: {type} {name}({args})\n'.format(
                type=cursor.result_type.spelling,
                name=cursor.spelling,
                args=', '.join(args))
        else:
            cdom = 'warning: unhandled cursor {kind} {name}\n'.format(
                kind=str(cursor.kind),
                name=cursor.spelling)

        doc_comment = compat_convert(doc_comment, options.get('compat'))
        doc_comment = indent(doc_comment, '   ')
        doc_comment = wrap_blank_lines(doc_comment)

        cdom += doc_comment

        meta = { 'line': comment.extent.start.line }
        meta['cursor.kind'] = cursor.kind
        meta['cursor.displayname'] = cursor.displayname
        meta['cursor.spelling'] = cursor.spelling

        result.append((cdom, meta))

        # FIXME: Needs some code deduplication with the above.
        if cursor.kind == CursorKind.STRUCT_DECL or cursor.kind == CursorKind.UNION_DECL:
            for c in cursor.get_children():
                if c.kind != CursorKind.FIELD_DECL:
                    # FIXME: handle nested unions
                    pass
#                    continue

                if c.hash not in comments:
                    continue
                comment = comments[c.hash]
                if not is_doc_comment(comment.spelling):
                    continue
                doc_comment = strip_comment(comment.spelling)

                # FIXME: this is sooo ugly, handles unnamed vs. named structs
                # in typedefs
                parent = cursor.spelling
                if parent == '':
                    parent = cursor.type.spelling
                # FIXME: do this recursively and smartly
                # FIXME: back references to parent definition
                cdom = '.. c:member:: {type} {parent}{sep}{member}\n'.format(
                    type=c.type.spelling,
                    parent=parent,
                    sep='.',
                    member=c.spelling)

                doc_comment = compat_convert(doc_comment, options.get('compat'))
                doc_comment = indent(doc_comment, '   ')
                doc_comment = wrap_blank_lines(doc_comment)

                cdom += doc_comment

                meta = { 'line': comment.extent.start.line }
                meta['cursor.kind'] = c.kind
                meta['cursor.displayname'] = c.displayname
                meta['cursor.spelling'] = c.spelling

                result.append((cdom, meta))
        elif cursor.kind == CursorKind.ENUM_DECL:
            for c in cursor.get_children():
                if c.hash not in comments:
                    continue
                comment = comments[c.hash]
                if not is_doc_comment(comment.spelling):
                    continue
                doc_comment = strip_comment(comment.spelling)

                # FIXME: parent enum name?
                cdom = '.. c:macro:: {name}\n'.format(name=c.spelling)

                doc_comment = compat_convert(doc_comment, options.get('compat'))
                doc_comment = indent(doc_comment, '   ')
                doc_comment = wrap_blank_lines(doc_comment)

                cdom += doc_comment

                meta = { 'line': comment.extent.start.line }
                meta['cursor.kind'] = c.kind
                meta['cursor.displayname'] = c.displayname
                meta['cursor.spelling'] = c.spelling

                result.append((cdom, meta))

    # sort to interleave top level comments back in place
    result.sort(key=lambda r: r[1]['line'])

    return result

def main():
    parser = argparse.ArgumentParser(description='Hawkmoth.')
    parser.add_argument('file', metavar='FILE', type=str, action='store',
                        help='tiedosto')
    parser.add_argument('--compat',
                        choices=['none',
                                 'javadoc-basic',
                                 'javadoc-liberal',
                                 'kernel-doc'],
                        help='compatibility options')
    parser.add_argument('--clang', metavar='PARAM[,PARAM,...]')
    parser.add_argument('--verbose', dest='verbose', action='store_true',
                        help='verbose output')
    args = parser.parse_args()

    filename = args.file

    comments = parse(filename, compat=args.compat, clang=args.clang)
    for (comment, meta) in comments:
        if args.verbose:
            print('# ' + str(meta))
        print(comment)

if __name__ == '__main__':
    main()
