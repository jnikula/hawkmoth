# Copyright (c) 2016-2023 Jani Nikula <jani@nikula.org>
# Copyright (c) 2018-2023 Bruno Santos <brunomanuelsantos@tecnico.ulisboa.pt>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

from clang.cindex import (
    TokenKind,
    CursorKind,
    TypeKind,
    StorageClass,
    AccessSpecifier,
    ExceptionSpecificationKind,
    SourceLocation,
    SourceRange,
)


class DocCursor:
    """Documentation centric wrapper for Clang's own ``Cursor``.

    This class abstracts a documentation worthy cursor so the user can query
    relevant bits for documentation purpose, but otherwise hide all the
    complications behind Clang's AST traversal and extraction of said bits of
    information.

    Technically, this class can hold any Clang cursor within itself, but it
    won't expose any relevant information for those.
    """

    def __init__(self, domain=None, cursor=None, comments=None):
        self._comments = comments if comments else {}
        self._cc = cursor

        self.domain = domain
        self.hash = self._cc.hash
        self.kind = self._cc.kind

        if self._cc.hash in self._comments:
            self.comment = self._comments[self._cc.hash]
        else:
            self.comment = None

        self.displayname = self._cc.displayname
        if self._cc.kind == CursorKind.ENUM_CONSTANT_DECL:
            if '=' in [t.spelling for t in self.get_tokens()]:
                self.enum_value = self._cc.enum_value
            else:
                self.enum_value = None
        self.is_scoped_enum = self._cc.is_scoped_enum
        self.spelling = self._cc.spelling
        self.type = self._cc.type

    def __hash__(self):
        return self._cc.hash

    def get_meta(self):
        return {
            'line': self.comment.extent.start.line if self.comment else '',
            'cursor.kind': self._cc.kind,
            'cursor.displayname': self._cc.displayname,
            'cursor.spelling': self._cc.spelling,
        }

    def get_children(self):
        """Get children cursors."""
        domain = self.domain

        # Identify `extern "C"` blocks and change domain accordingly. For some
        # reason, the Python bindings don't return the cursor kind LINKAGE_SPEC
        # as one would expect, so we need to do it the hard way.
        if domain == 'cpp' and self.kind == CursorKind.UNEXPOSED_DECL:
            tokens = self.get_tokens()
            ntoken = next(tokens, None)
            if ntoken and ntoken.spelling == 'extern':
                ntoken = next(tokens, None)
                if ntoken and ntoken.spelling == '"C"':
                    domain = 'c'

        for c in self._cc.get_children():
            yield DocCursor(domain=domain, cursor=c, comments=self._comments)

    def get_tokens(self):
        """Get cursor tokens.

        Wrapper for Clang's `cursor.get_tokens()` that addresses issues for
        cursors whose extent contains macro expansions. The result may be empty
        or contain bogus tokens, depending on the case.

        The problem seems to be related to `cursor.extent`. Recreating the
        extent and getting the tokens from the translation unit works fine. The
        `__repr__` for both the recreated and original extents is the same, but
        comparison indicates they do differ under the hood.
        """
        tu = self._cc.translation_unit

        start = self._cc.extent.start
        start = SourceLocation.from_position(tu, start.file, start.line, start.column)

        end = self._cc.extent.end
        end = SourceLocation.from_position(tu, end.file, end.line, end.column)

        extent = SourceRange.from_locations(start, end)

        yield from tu.get_tokens(extent=extent)

    def var_type_fixup(self):
        """Fix non trivial variable and argument types.

        If this is an array, the dimensions should be applied to the name, not
        the type. If this is a function pointer, or an array of function
        pointers, the name should be within the parenthesis as in ``(*name)``
        or ``(*name[N])``.
        """
        return self._var_type_fixup(self)

    def get_args(self):
        """Get function / method arguments."""
        args = []

        # Only fully prototyped functions will have argument lists to process.
        if self._cc.type.kind == TypeKind.FUNCTIONPROTO:
            for c in self.get_children():
                if c._cc.kind == CursorKind.PARM_DECL:
                    arg_ttype, arg_name = self._var_type_fixup(c)
                    args.extend([(arg_ttype, arg_name)])

            if self._cc.type.is_function_variadic():
                args.extend([('', '...')])
            if len(args) == 0:
                args.extend([('', 'void')])

        return args

    def function_fixup(self):
        """Parse additional details of a function declaration."""
        args = self.get_args()

        full_type = self._get_function_quals()

        template_line = self._get_template_line()
        if template_line:
            full_type.append(template_line)

        full_type.append(self._normalize_type(self._cc.result_type.spelling))

        ttype = ' '.join(full_type)

        return ttype, args

    def method_fixup(self):
        """Parse additional details of a method declaration."""
        args = self.get_args()

        full_type = []

        access_spec = self._get_access_specifier()
        if access_spec:
            full_type.append(access_spec)

        pre_quals, pos_quals = self._get_method_quals()

        full_type.extend(pre_quals)

        template_line = self._get_template_line()
        if template_line:
            full_type.append(template_line)

        if self._cc.kind not in [CursorKind.CONSTRUCTOR, CursorKind.DESTRUCTOR]:
            full_type.append(self._cc.result_type.spelling)

        ttype = ' '.join(full_type)
        quals = ' '.join(pos_quals)

        return ttype, args, quals

    def type_definition_fixup(self):
        """Fix non trivial type definitions."""
        type_elem = []

        # Short cut for anonymous symbols.
        if self._cc.is_anonymous():
            return None

        # libclang 16 and later have cursor.spelling == cursor.type.spelling
        # for typedefs of anonymous entities, while libclang 15 and earlier
        # have an empty string. Match the behaviour across libclang versions.
        if self._cc.spelling == '':
            return self._cc.type.spelling

        type_elem.extend(self._specifiers_fixup(self._cc.type))

        colon_suffix = ''
        if self._cc.kind in [CursorKind.STRUCT_DECL,
                             CursorKind.CLASS_DECL,
                             CursorKind.CLASS_TEMPLATE]:
            inheritance = self._get_inheritance()
            if inheritance:
                colon_suffix = inheritance
        elif self._cc.kind == CursorKind.ENUM_DECL:
            scopedenum_type = self._get_scopedenum_type()
            if scopedenum_type:
                colon_suffix = scopedenum_type

        template = self._get_template_line()
        template = template + ' ' if template else ''

        return f'{template}{self._cc.spelling}{colon_suffix}'

    def get_macro_args(self):
        """Get macro arguments.

        Returns:
            None for simple macros, a potentially empty list of arguments for
            function-like macros
        """
        if self._cc.kind != CursorKind.MACRO_DEFINITION:
            return None

        tokens = self.get_tokens()

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

    def _symbolic_dims(self):
        dim = None
        for spelling in [t.spelling for t in self.get_tokens()]:
            if spelling == '[':
                # dim should be None here
                dim = []
            elif spelling == ']':
                # dim should not be None here
                yield ' '.join(dim)
                dim = None
            elif dim is not None:
                dim.append(spelling)

    def _dims_fixup(self, dims):
        if not dims:
            return ''

        symbolic_dims = list(self._symbolic_dims())
        if len(symbolic_dims) == len(dims):
            dims = symbolic_dims

        return ''.join([f'[{d}]' for d in dims])

    def _get_storage_class(self):
        """Get the storage class of a cursor.

        Only storage classes that are relevant to the documentation are
        returned.

        Returns:
            Storage class as a string. ``None`` otherwise.
        """
        storage_class_map = {
            StorageClass.EXTERN: 'extern',
            StorageClass.STATIC: 'static',
        }

        return storage_class_map.get(self._cc.storage_class)

    def _get_function_quals(self):
        """Get all the qualifiers of a function object.

        Returns:
            List of (prefix) function qualifiers.
        """
        tokens = [t.spelling for t in self.get_tokens()]
        quals = []

        if 'static' in tokens:
            quals.append('static')
        if 'inline' in tokens:
            quals.append('inline')

        return quals

    def _get_method_quals(self):
        """Get all the qualifiers of a method.

        Returns:
            List of prefix method qualifiers and list of suffix method
            qualifiers.
        """
        tokens = [t.spelling for t in self.get_tokens()]
        pre_quals = []
        pos_quals = []

        if self._cc.is_static_method():
            pre_quals.append('static')
        if self._cc.is_virtual_method():
            pre_quals.append('virtual')
        if 'constexpr' in tokens:
            pre_quals.append('constexpr')

        if self._cc.is_const_method():
            pos_quals.append('const')
        if self._cc.is_pure_virtual_method():
            pos_quals.append('= 0')
        if self._cc.is_default_method():
            pos_quals.append('= default')
        if 'delete' in tokens:
            pos_quals.append('= delete')
        if 'override' in tokens:
            pos_quals.append('override')

        except_spec = self._cc.exception_specification_kind
        if except_spec == ExceptionSpecificationKind.BASIC_NOEXCEPT:
            pos_quals.append('noexcept')

        return pre_quals, pos_quals

    def _specifiers_fixup(self, basetype):
        """Fix the type for C++ specifiers.

        Note the ``basetype`` is not necessarily ``cursor.type``. When dealing
        with pointers or arrays, we need to get to the base type as in
        :py:func:`_var_type_fixup`.

        Returns:
            List of C++ specifiers for the cursor.
        """
        tokens = [t.spelling for t in self.get_tokens()]
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

    def _get_access_specifier(self):
        """Get the access specifier of a cursor, if any.

        Returns:
            One of 'private', 'protected', 'public' or `None`.
        """
        # No access specifiers in C.
        if self.domain == 'c':
            return None

        # No access specifiers in redundant contexts.
        if self._cc.semantic_parent:
            if self._cc.semantic_parent.kind == CursorKind.UNION_DECL:
                return None

        name_map = {
            AccessSpecifier.PRIVATE: 'private',
            AccessSpecifier.PROTECTED: 'protected',
            AccessSpecifier.PUBLIC: 'public',
        }

        return name_map.get(self._cc.access_specifier, None)

    def _get_template_line(self):
        """Get the template arguments of a cursor.

        This recurses for templated template arguments.

        Returns:
            String with the form 'template<...> ' if the cursor is a template
            or `None` otherwise. When the cursor represents a templated
            template argument, the returned string is actually of the form
            'template<...> name', but this should only occur under recursion.
        """
        # We only add the name when we recurse, in which case we need to track
        # the name of the templated template argument. Otherwise the name is
        # not part of the template arguments.
        name = ''

        if self._cc.kind not in [CursorKind.CLASS_TEMPLATE,
                                 CursorKind.FUNCTION_TEMPLATE,
                                 CursorKind.TEMPLATE_TEMPLATE_PARAMETER]:
            return None

        # The type of type parameters can be 'typename' and 'class'. These are
        # equivalent, but we want it to look like the source code for
        # consistency. We can do it by looking at the tokens directly. This is
        # slightly complicated due to variadic template type parameters.
        def typetype(cursor):
            tokens = list(cursor.get_tokens())
            if tokens[-2].spelling == '...':
                return f'{tokens[-3].spelling}...'
            else:
                return f'{tokens[-2].spelling}'

        # We need to add the keyword 'typename' or 'class' if we have recursed
        # and therefore we are inside the template argument list.
        if self._cc.kind == CursorKind.TEMPLATE_TEMPLATE_PARAMETER:
            name = f' {typetype(self)} {self._cc.spelling}'

        template_args = []
        for child in self.get_children():
            if child._cc.kind == CursorKind.TEMPLATE_TYPE_PARAMETER:
                template_args.append(f'{typetype(child)} {child._cc.spelling}')
            elif child._cc.kind == CursorKind.TEMPLATE_NON_TYPE_PARAMETER:
                arg_name = f' {child._cc.spelling}' if child._cc.spelling != '' else '...'
                template_args.append(f'{child._cc.type.spelling}{arg_name}')
            elif child._cc.kind == CursorKind.TEMPLATE_TEMPLATE_PARAMETER:
                arg = child._get_template_line()
                if arg:
                    template_args.append(arg)

        return f'template<{", ".join(template_args)}>{name}'

    def _get_inheritance(self):
        """Get the full inheritance list of a cursor in C++ syntax.

        Returns:
            String with the form ': A, B, ...' when a cursor has
            `CXX_BASE_SPECIFIER` children or `None` otherwise.
        """
        inherited = []
        for child in self.get_children():
            if child._cc.kind == CursorKind.CXX_BASE_SPECIFIER:
                pad = lambda s: s + ' ' if s else ''
                access_spec = child._get_access_specifier()
                inherited.append(f'{pad(access_spec)}{child._cc.type.spelling}')

        return ': ' + ', '.join(inherited) if len(inherited) > 0 else None

    def _get_scopedenum_type(self):
        """Get the explicit underlying type of a scoped enumerator.

        Returns:
            Underlying type of a scoped enumerator that has been explicitly
            defined. ``None`` otherwise.
        """
        if self._cc.kind == CursorKind.ENUM_DECL and self._cc.is_scoped_enum():
            if list(self.get_tokens())[3].spelling == ':':
                return f': {self._cc.enum_type.spelling}'
        return None

    @staticmethod
    def _normalize_type(type_string):
        return 'bool' if type_string == '_Bool' else type_string

    @staticmethod
    def _var_type_fixup(cursor):
        cursor_type = cursor._cc.type

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

        dims = cursor._dims_fixup(dims)

        type_elem = []

        access_spec = cursor._get_access_specifier()
        if access_spec:
            type_elem.append(access_spec)

        if cursor_type.kind == TypeKind.FUNCTIONPROTO:
            pad = lambda s: s if s.endswith('*') or s.endswith('&') else s + ' '

            args = []
            for c in cursor.get_children():
                if c._cc.kind == CursorKind.PARM_DECL:
                    arg_ttype, arg_name = cursor._var_type_fixup(c)
                    args.append(f'{pad(arg_ttype)}{arg_name}' if arg_name else arg_ttype)
            if cursor_type.is_function_variadic():
                args.append('...')
            if len(args) == 0:
                args.append('void')

            ret_type = cursor._normalize_type(cursor_type.get_result().spelling)

            name = f'''{pad(ret_type)}({pad(stars_and_quals)}{cursor._cc.spelling}{dims})({', '.join(args)})'''  # noqa: E501
        else:

            storage_class = cursor._get_storage_class()
            if storage_class:
                type_elem.append(storage_class)

            type_elem.extend(cursor._specifiers_fixup(cursor_type))

            if stars_and_quals:
                type_elem.append(stars_and_quals)

            name = cursor._cc.spelling + dims

        # Convert _Bool to bool
        type_elem = [cursor._normalize_type(t) for t in type_elem]

        ttype = ' '.join(type_elem)
        return ttype, name
