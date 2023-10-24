

from clang.cindex import TokenKind, CursorKind, TypeKind
from clang.cindex import StorageClass, AccessSpecifier, ExceptionSpecificationKind
from clang.cindex import SourceLocation, SourceRange

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
    if cursor.is_anonymous():
        return None

    # libclang 16 and later have cursor.spelling == cursor.type.spelling for
    # typedefs of anonymous entities, while libclang 15 and earlier have an
    # empty string. Match the behaviour across libclang versions.
    if cursor.spelling == '':
        return cursor.type.spelling

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
