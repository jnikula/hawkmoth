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

from clang.cindex import TokenKind, CursorKind, TypeKind
from clang.cindex import StorageClass, AccessSpecifier, ExceptionSpecificationKind
from clang.cindex import Index, TranslationUnit, TranslationUnitLoadError
from clang.cindex import Diagnostic
from clang.cindex import SourceLocation, SourceRange

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

# Workaround for clang cursor.get_tokens() being unreliable for cursors whose
# extent contains macro expansions. The result may be empty or contain bogus
# tokens, depending on the case.
#
# The problem seems to be related to cursor.extent. Recreating the extent and
# getting the tokens from the translation unit works fine. The __repr__ for both
# the recreated and original extents is the same, but comparison indicates they
# do differ under the hood.
def _cursor_get_tokens(cursor):
    tu = cursor.translation_unit

    start = cursor.extent.start
    start = SourceLocation.from_position(tu, start.file, start.line, start.column)

    end = cursor.extent.end
    end = SourceLocation.from_position(tu, end.file, end.line, end.column)

    extent = SourceRange.from_locations(start, end)

    yield from tu.get_tokens(extent=extent)

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

    tokens = _cursor_get_tokens(cursor)

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

def _get_function_quals(cursor):
    """Get all the qualifiers of a function object.

    Returns:
        List of (prefix) function qualifiers.
    """
    tokens = [t.spelling for t in _cursor_get_tokens(cursor)]
    quals = []

    if 'static' in tokens:
        quals.append('static')
    if 'inline' in tokens:
        quals.append('inline')

    return quals

def _get_method_quals(cursor):
    """Get all the qualifiers of a method.

    Returns:
        List of prefix method qualifiers and list of suffix method qualifiers.
    """
    tokens = [t.spelling for t in _cursor_get_tokens(cursor)]
    pre_quals = []
    pos_quals = []

    if cursor.is_static_method():
        pre_quals.append('static')
    if cursor.is_virtual_method():
        pre_quals.append('virtual')
    if 'constexpr' in tokens:
        pre_quals.append('constexpr')

    if cursor.is_const_method():
        pos_quals.append('const')
    if cursor.is_pure_virtual_method():
        pos_quals.append('= 0')
    if cursor.is_default_method():
        pos_quals.append('= default')
    if 'delete' in tokens:
        pos_quals.append('= delete')
    if 'override' in tokens:
        pos_quals.append('override')

    except_spec = cursor.exception_specification_kind
    if except_spec == ExceptionSpecificationKind.BASIC_NOEXCEPT:
        pos_quals.append('noexcept')

    return pre_quals, pos_quals

def _get_access_specifier(cursor, domain='cpp'):
    """Get the access specifier of a cursor, if any.

    Returns:
        One of 'private', 'protected', 'public' or `None`.
    """
    # No access specifiers in C.
    if domain == 'c':
        return None

    # No access specifiers in redundant contexts.
    if cursor.semantic_parent and cursor.semantic_parent.kind == CursorKind.UNION_DECL:
        return None

    name_map = {
        AccessSpecifier.PRIVATE: 'private',
        AccessSpecifier.PROTECTED: 'protected',
        AccessSpecifier.PUBLIC: 'public',
    }

    return name_map.get(cursor.access_specifier, None)

def _get_template_line(cursor):
    """Get the template arguments of a cursor.

    This recurses for templated template arguments.

    Returns:
        String with the form 'template<...> ' if the cursor is a template or
        `None` otherwise. When the cursor represents a templated template
        argument, the returned string is actually of the form 'template<...>
        name', but this should only occur under recursion.
    """
    # We only add the name when we recurse, in which case we need to track the
    # name of the templated template argument. Otherwise the name is not part of
    # the template arguments.
    name = ''

    if cursor.kind not in [CursorKind.CLASS_TEMPLATE,
                           CursorKind.FUNCTION_TEMPLATE,
                           CursorKind.TEMPLATE_TEMPLATE_PARAMETER]:
        return None

    # The type of type parameters can be 'typename' and 'class'. These are
    # equivalent, but we want it to look like the source code for consistency.
    # We can do it by looking at the tokens directly. This is slightly
    # complicated due to variadic template type parameters.
    def typetype(cursor):
        tokens = list(_cursor_get_tokens(cursor))
        if tokens[-2].spelling == '...':
            return f'{tokens[-3].spelling}...'
        else:
            return f'{tokens[-2].spelling}'

    # We need to add the keyword 'typename' or 'class' if we have recursed and
    # therefore we are inside the template argument list.
    if cursor.kind == CursorKind.TEMPLATE_TEMPLATE_PARAMETER:
        name = f' {typetype(cursor)} {cursor.spelling}'

    template_args = []
    for child in cursor.get_children():
        if child.kind == CursorKind.TEMPLATE_TYPE_PARAMETER:
            template_args.append(f'{typetype(child)} {child.spelling}')
        elif child.kind == CursorKind.TEMPLATE_NON_TYPE_PARAMETER:
            arg_name = f' {child.spelling}' if child.spelling != '' else '...'
            template_args.append(f'{child.type.spelling}{arg_name}')
        elif child.kind == CursorKind.TEMPLATE_TEMPLATE_PARAMETER:
            arg = _get_template_line(child)
            if arg:
                template_args.append(arg)

    return f'template<{", ".join(template_args)}>{name}'

def _specifiers_fixup(cursor, basetype):
    """Fix the type for C++ specifiers.

    Note the ``basetype`` is not necessarily ``cursor.type``. When dealing with
    pointers or arrays, we need to get to the base type as in
    :py:func:`_var_type_fixup`.

    Returns:
        List of C++ specifiers for the cursor.
    """
    tokens = [t.spelling for t in _cursor_get_tokens(cursor)]
    type_elem = []

    if 'mutable' in tokens:
        type_elem.append('mutable')

    # If 'constexpr', strip the redundant 'const' that Clang adds to the
    # type spelling by default.
    if 'constexpr' in tokens:
        type_elem.append('constexpr')
        type_elem.append(basetype.spelling[len('const '):])
    else:
        type_elem.append(basetype.spelling)

    return type_elem

def _get_scopedenum_type(cursor):
    """Get the explicit underlying type of a scoped enumerator.

    Returns:
        Underlying type of a scoped enumerator that has been explicitly defined.
        ``None`` otherwise.
    """
    if cursor.kind == CursorKind.ENUM_DECL and cursor.is_scoped_enum():
        if list(_cursor_get_tokens(cursor))[3].spelling == ':':
            return f': {cursor.enum_type.spelling}'
    return None

def _normalize_type(type_string):
    return 'bool' if type_string == '_Bool' else type_string

def _symbolic_dims(cursor):
    dim = None
    for spelling in [t.spelling for t in _cursor_get_tokens(cursor)]:
        if spelling == '[':
            # dim should be None here
            dim = []
        elif spelling == ']':
            # dim should not be None here
            yield ' '.join(dim)
            dim = None
        elif dim is not None:
            dim.append(spelling)

def _dims_fixup(cursor, dims):
    if not dims:
        return ''

    symbolic_dims = list(_symbolic_dims(cursor))
    if len(symbolic_dims) == len(dims):
        dims = symbolic_dims

    return ''.join([f'[{d}]' for d in dims])

def _var_type_fixup(cursor, domain):
    """Fix non trivial variable and argument types.

    If this is an array, the dimensions should be applied to the name, not
    the type.
    If this is a function pointer, or an array of function pointers, the
    name should be within the parenthesis as in ``(*name)`` or ``(*name[N])``.
    """
    cursor_type = cursor.type

    stars_and_quals = ''
    dims = []
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
            dims.append(cursor_type.element_count)
            cursor_type = cursor_type.get_array_element_type()
        elif cursor_type.kind == TypeKind.INCOMPLETEARRAY:
            dims.append('')
            cursor_type = cursor_type.get_array_element_type()
        else:
            break

    dims = _dims_fixup(cursor, dims)

    type_elem = []

    access_spec = _get_access_specifier(cursor, domain)
    if access_spec:
        type_elem.append(access_spec)

    if cursor_type.kind == TypeKind.FUNCTIONPROTO:
        pad = lambda s: s if s.endswith('*') or s.endswith('&') else s + ' '

        args = []
        for c in cursor.get_children():
            if c.kind == CursorKind.PARM_DECL:
                arg_ttype, arg_name = _var_type_fixup(c, domain)
                args.append(f'{pad(arg_ttype)}{arg_name}' if arg_name else arg_ttype)
        if cursor_type.is_function_variadic():
            args.append('...')
        if len(args) == 0:
            args.append('void')

        ret_type = _normalize_type(cursor_type.get_result().spelling)

        name = f'''{pad(ret_type)}({pad(stars_and_quals)}{cursor.spelling}{dims})({', '.join(args)})'''  # noqa: E501
    else:

        storage_class = _get_storage_class(cursor)
        if storage_class:
            type_elem.append(storage_class)

        type_elem.extend(_specifiers_fixup(cursor, cursor_type))

        if stars_and_quals:
            type_elem.append(stars_and_quals)

        name = cursor.spelling + dims

    # Convert _Bool to bool
    type_elem = [_normalize_type(t) for t in type_elem]

    ttype = ' '.join(type_elem)
    return ttype, name

def _type_definition_fixup(cursor):
    """Fix non trivial type definitions."""
    type_elem = []

    # Short cut for anonymous symbols.
    if cursor.spelling == '':
        return None

    type_elem.extend(_specifiers_fixup(cursor, cursor.type))

    colon_suffix = ''
    if cursor.kind in [CursorKind.STRUCT_DECL,
                       CursorKind.CLASS_DECL,
                       CursorKind.CLASS_TEMPLATE]:
        inheritance = _get_inheritance(cursor)
        if inheritance:
            colon_suffix = inheritance
    elif cursor.kind == CursorKind.ENUM_DECL:
        scopedenum_type = _get_scopedenum_type(cursor)
        if scopedenum_type:
            colon_suffix = scopedenum_type

    template = _get_template_line(cursor)
    template = template + ' ' if template else ''

    return f'{template}{cursor.spelling}{colon_suffix}'

def _get_args(cursor, domain):
    """Get function / method arguments."""
    args = []

    # Only fully prototyped functions will have argument lists to process.
    if cursor.type.kind == TypeKind.FUNCTIONPROTO:
        for c in cursor.get_children():
            if c.kind == CursorKind.PARM_DECL:
                arg_ttype, arg_name = _var_type_fixup(c, domain)
                args.extend([(arg_ttype, arg_name)])

        if cursor.type.is_function_variadic():
            args.extend([('', '...')])
        if len(args) == 0:
            args.extend([('', 'void')])

    return args

def _function_fixup(cursor, domain):
    """Parse additional details of a function declaration."""
    args = _get_args(cursor, domain)

    full_type = _get_function_quals(cursor)

    template_line = _get_template_line(cursor)
    if template_line:
        full_type.append(template_line)

    full_type.append(_normalize_type(cursor.result_type.spelling))

    ttype = ' '.join(full_type)

    return ttype, args

def _method_fixup(cursor):
    """Parse additional details of a method declaration."""
    args = _get_args(cursor, 'cpp')

    full_type = []

    access_spec = _get_access_specifier(cursor)
    if access_spec:
        full_type.append(access_spec)

    pre_quals, pos_quals = _get_method_quals(cursor)

    full_type.extend(pre_quals)

    template_line = _get_template_line(cursor)
    if template_line:
        full_type.append(template_line)

    if cursor.kind not in [CursorKind.CONSTRUCTOR, CursorKind.DESTRUCTOR]:
        full_type.append(cursor.result_type.spelling)

    ttype = ' '.join(full_type)
    quals = ' '.join(pos_quals)

    return ttype, args, quals

def _get_inheritance(cursor):
    """Get the full inheritance list of a cursor in C++ syntax.

    Returns:
        String with the form ': A, B, ...' when a cursor has
        `CXX_BASE_SPECIFIER` children or `None` otherwise.
    """
    inherited = []
    for child in cursor.get_children():
        if child.kind == CursorKind.CXX_BASE_SPECIFIER:
            pad = lambda s: s + ' ' if s else ''
            access_spec = _get_access_specifier(child)
            inherited.append(f'{pad(access_spec)}{child.type.spelling}')

    return ': ' + ', '.join(inherited) if len(inherited) > 0 else None

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
        ttype, decl_name = _var_type_fixup(cursor, domain)

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

    elif cursor.kind in [CursorKind.STRUCT_DECL,
                         CursorKind.UNION_DECL,
                         CursorKind.ENUM_DECL,
                         CursorKind.CLASS_DECL,
                         CursorKind.CLASS_TEMPLATE]:

        decl_name = _type_definition_fixup(cursor)

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
        # Show enumerator value if it's explicitly set in source
        if '=' in [t.spelling for t in _cursor_get_tokens(cursor)]:
            value = cursor.enum_value
        else:
            value = None

        ds = docstring.EnumeratorDocstring(domain=domain, name=name,
                                           value=value, text=text,
                                           meta=meta, nest=nest)

        return [ds]

    elif cursor.kind == CursorKind.FUNCTION_DECL:
        ttype, args = _function_fixup(cursor, domain)
        ds = docstring.FunctionDocstring(domain=domain, text=text,
                                         nest=nest, name=name,
                                         ttype=ttype, args=args,
                                         quals='', meta=meta)
        return [ds]

    elif cursor.kind in [CursorKind.CONSTRUCTOR,
                         CursorKind.DESTRUCTOR,
                         CursorKind.CXX_METHOD,
                         CursorKind.FUNCTION_TEMPLATE]:
        ttype, args, quals = _method_fixup(cursor)
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
