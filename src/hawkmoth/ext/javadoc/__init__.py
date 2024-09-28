# Copyright (c) 2023, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import re
from typing import Optional

# The "operator" character, either \ or @, but not escaped with \
OP = r'(?<!\\)(?P<op>[\\@])'

class _handler:
    """Base class for all command handlers."""
    _indented_paragraph = False

    def __init__(self, app=None, indent=None, op=None, command=None, rest=None):
        self._app = app
        self._indent = indent
        self._op = op
        self._command = command
        self._rest = rest

    def blank_line_ends(self):
        """Does a blank line end this command?"""
        return True

    def command_ends(self, command):
        """Does the provided command end this command?"""
        return True

    @staticmethod
    def _inline_markup(line):
        """Handle inline markup."""

        word_regex = r'[^\s.]+'
        tagged_phrase_regex = r'[^<]*'

        # italics: \a \e \em <em>...</em>
        line = re.sub(fr'{OP}(a|e|em)\s+(?P<markup>{word_regex})', r'*\g<markup>*', line)
        line = re.sub(fr'<em>(?P<markup>{tagged_phrase_regex})</em>', r'*\g<markup>*', line)

        # bold: \b <b>...</b>
        line = re.sub(fr'{OP}b\s+(?P<markup>{word_regex})', r'**\g<markup>**', line)
        line = re.sub(fr'<b>(?P<markup>{tagged_phrase_regex})</b>', r'**\g<markup>**', line)

        # monospace: \c \p <tt>...</tt>
        line = re.sub(fr'{OP}(c|p)\s+(?P<markup>{word_regex})', r'``\g<markup>``', line)
        line = re.sub(fr'<tt>(?P<markup>{tagged_phrase_regex})</tt>', r'``\g<markup>``', line)

        # references to previous anchors
        # FIXME: link title
        line = re.sub(fr'{OP}ref\s+(?P<ref>\w+)', r':ref:`\g<ref>`', line)

        # FIXME:
        # - copybrief
        # - copydetails
        # - emoji
        # - f
        # - n

        return line

    def rest(self):
        """Return the "rest" of the line after @command."""
        return self._inline_markup(self._rest)

    def header(self):
        """Convert the first line of this command."""
        yield ''

    def convert(self, line):
        """Convert a regular line within this paragraph."""
        line = self._inline_markup(line)

        if self._indented_paragraph:
            line = f'   {line}'

        yield line

class _plain(_handler):
    pass

class _not_implemented(_plain):
    """Placeholder for commands that have not been implemented."""
    # FIXME: warn about not implemented commands
    pass

class _block_with_end_command(_handler):
    """Paragraph with a dedicated command to end it.

    For example, @code/@endcode."""
    _end_command: Optional[str] = None

    def end_command(self):
        """Get the name of the command that ends this paragraph."""
        return self._end_command if self._end_command else f'end{self._command}'

    def blank_line_ends(self):
        return False

    def command_ends(self, command):
        return self.end_command() == command

class _ignore_until_end_command(_block_with_end_command):
    """Ignore the paragraph until dedicated command ends it."""
    # FIXME: warn about ignored commands
    def header(self):
        yield ''

    def convert(self, line):
        yield ''

class _startuml(_ignore_until_end_command):
    # Needed because it's @startuml/@enduml, not @uml/@enduml.
    _end_command = 'enduml'

class _code(_block_with_end_command):
    def header(self):
        yield ''
        yield '.. code-block::'
        yield ''

    def convert(self, line):
        yield f'   {line}'

class _anchor(_handler):
    def header(self):
        anchor = self._rest.strip()

        yield ''
        yield f'.. {anchor}:'
        yield ''

class _strip_command(_handler):
    """Strip command, treat everything else as normal."""
    def header(self):
        yield f'{self._indent}{self.rest().strip()}'

class _field_list(_handler):
    """Paragraph which becomes a single field list item."""
    _field_name: Optional[str] = None
    _indented_paragraph = True

    def field_name(self):
        return self._field_name if self._field_name else self._command

    def header(self):
        yield ''
        yield f'{self._indent}:{self.field_name()}:{self.rest()}'

class _author(_field_list):
    _field_name = 'author'

class _return(_field_list):
    _field_name = 'return'

class _see(_field_list):
    _field_name = 'see'

class _param(_field_list):
    """Parameter description."""
    _field_name = 'param'

    def header(self):
        mo = re.match(r'^((?P<sp0>\s*)\[(?P<direction>[a-zA-Z, ]+)\])?(?P<sp1>\s*)(?P<name>([a-zA-Z0-9_]+|\.\.\.))(?P<sp2>\s*(?P<desc>.*))',  # noqa: E501
                      self.rest())
        if mo is None:
            # FIXME
            yield ''
            return

        direction = mo.group('direction')
        name = mo.group('name')
        desc = mo.group('desc')

        yield ''
        if direction:
            yield f'{self._indent}:param {name}: **[{direction}]** {desc}'
        else:
            yield f'{self._indent}:param {name}: {desc}'

class _admonition(_handler):
    """Admonitions such as @note and @warning."""
    _indented_paragraph = True
    _directive = None

    def directive(self):
        return self._directive if self._directive else self._command

    def header(self):
        yield ''
        yield f'.. {self.directive()}::'
        yield ''
        rest = self.rest().strip()
        if rest:
            yield f'   {rest}'

# Map non-inline commands to handler classes.
#
# All the non-inline commands in the order listed at
# https://www.doxygen.nl/manual/commands.html
_handlers = {
    # structural indicators
    'addtogroup': _not_implemented,
    'callgraph': _not_implemented,
    'hidecallgraph': _not_implemented,
    'callergraph': _not_implemented,
    'hidecallergraph': _not_implemented,
    'showrefby': _not_implemented,
    'hiderefby': _not_implemented,
    'showrefs': _not_implemented,
    'hiderefs': _not_implemented,
    'showinlinesource': _not_implemented,
    'hideinlinesource': _not_implemented,
    'includegraph': _not_implemented,
    'hideincludegraph': _not_implemented,
    'includedbygraph': _not_implemented,
    'hideincludedbygraph': _not_implemented,
    'directorygraph': _not_implemented,
    'hidedirectorygraph': _not_implemented,
    'collaborationgraph': _not_implemented,
    'hidecollaborationgraph': _not_implemented,
    'inheritancegraph': _not_implemented,
    'hideingeritancegraph': _not_implemented,
    'groupgraph': _not_implemented,
    'hidegroupgraph': _not_implemented,
    'qualifier': _not_implemented,
    'category': _not_implemented,
    'class': _not_implemented,  # WARN
    'concept': _not_implemented,
    'def': _not_implemented,  # WARN
    'defgroup': _not_implemented,
    'dir': _not_implemented,
    'enum': _not_implemented,  # WARN
    'example': _not_implemented,  # FIXME
    'endinternal': _not_implemented,  # WARN
    'extends': _not_implemented,  # FIXME
    'file': _not_implemented,  # FIXME
    'fileinfo': _not_implemented,
    'lineinfo': _not_implemented,  # WARN
    'fn': _not_implemented,  # WARN
    'headerfile': _not_implemented,
    'hideinitializer': _not_implemented,
    'idlexcept': _not_implemented,
    'implements': _not_implemented,
    'ingroup': _not_implemented,
    'interface': _not_implemented,  # WARN
    'internal': _not_implemented,
    'mainpage': _not_implemented,  # FIXME
    'memberof': _not_implemented,
    'module': _not_implemented,
    'name': _not_implemented,
    'namespace': _not_implemented,
    'nosubgrouping': _not_implemented,
    'overload': _not_implemented,
    'package': _not_implemented,
    'page': _not_implemented,  # FIXME
    'private': _not_implemented,
    'privatesection': _not_implemented,
    'property': _not_implemented,
    'protected': _not_implemented,
    'protectedsection': _not_implemented,
    'protocol': _not_implemented,
    'public': _not_implemented,
    'publicsection': _not_implemented,
    'pure': _not_implemented,
    'relates': _not_implemented,  # FIXME
    'related': _not_implemented,  # FIXME
    'relatesalso': _not_implemented,
    'relatedalso': _not_implemented,
    'showinitializer': _not_implemented,
    'static': _not_implemented,
    'typedef': _not_implemented,  # WARN
    'union': _not_implemented,  # WARN
    'var': _not_implemented,  # WARN
    'vhdlflow': _not_implemented,
    'weakgroup': _not_implemented,
    # section indicators
    'attention': _admonition,
    'author': _author,
    'authors': _author,
    'brief': _strip_command,
    'bug': _field_list,
    'cond': _not_implemented,
    'copyright': _field_list,
    'date': _field_list,
    'showdate': _not_implemented,
    'deprecated': _field_list,
    'details': _strip_command,
    'noop': _not_implemented,
    'raisewarning': _not_implemented,
    'else': _not_implemented,
    'elseif': _not_implemented,
    'endcond': _not_implemented,
    'endif': _not_implemented,
    'exception': _field_list,
    'if': _not_implemented,
    'ifnot': _not_implemented,
    'invariant': _field_list,
    'note': _admonition,
    'par': _not_implemented,
    'param': _param,
    'parblock': _not_implemented,
    'endparblock': _not_implemented,
    'tparam': _field_list,
    'post': _field_list,
    'pre': _field_list,
    'remark': _field_list,
    'remarks': _field_list,
    'result': _return,
    'return': _return,
    'returns': _return,
    'retval': _return,
    'sa': _see,
    'see': _see,
    'short': _strip_command,
    'since': _field_list,
    'test': _field_list,
    'throw': _field_list,
    'throws': _field_list,
    'todo': _field_list,
    'version': _field_list,
    'warning': _admonition,
    'xrefitem': _not_implemented,
    'addindex': _not_implemented,
    'anchor': _anchor,
    'cite': _field_list,
    'endlink': _not_implemented,
    'link': _not_implemented,
    'refitem': _not_implemented,
    'secreflist': _not_implemented,
    'endsecreflist': _not_implemented,
    'subpage': _not_implemented,
    'tableofcontents': _not_implemented,
    'section': _not_implemented,
    'subsection': _not_implemented,
    'subsubsection': _not_implemented,
    'paragraph': _not_implemented,
    'dontinclude': _not_implemented,
    'include': _not_implemented,
    'includelineno': _not_implemented,
    'includedoc': _not_implemented,
    'line': _not_implemented,
    'skip': _not_implemented,
    'skipline': _not_implemented,
    'snippet': _not_implemented,
    'snippetlineno': _not_implemented,
    'snippetdoc': _not_implemented,
    'until': _not_implemented,
    'verbinclude': _not_implemented,
    'htmlinclude': _not_implemented,
    'latexinclude': _not_implemented,
    'rtfinclude': _not_implemented,
    'maninclude': _not_implemented,
    'docbookinclude': _not_implemented,
    'xmlinclude': _not_implemented,
    # visual enhancements
    'arg': _not_implemented,  # FIXME
    'code': _code,
    'copydoc': _not_implemented,
    'docbookonly': _ignore_until_end_command,
    'dot': _ignore_until_end_command,
    'msc': _ignore_until_end_command,
    'startuml': _startuml,
    'dotfile': _not_implemented,
    'mscfile': _not_implemented,
    'diafile': _not_implemented,
    'doxyconfig': _not_implemented,
    'endcode': _plain,
    'enddocbookonly': _plain,
    'enddot': _plain,
    'endmsc': _plain,
    'enduml': _plain,
    'endhtmlonly': _plain,
    'endlatexonly': _plain,
    'endmanonly': _plain,
    'endrtfonly': _plain,
    'endverbatim': _plain,
    'endxmlonly': _plain,
    'htmlonly': _ignore_until_end_command,
    'image': _not_implemented,  # FIXME
    'latexonly': _ignore_until_end_command,
    'manonly': _ignore_until_end_command,
    'li': _not_implemented,  # FIXME
    'rtfonly': _ignore_until_end_command,
    'verbatim': _code,
    'xmlonly': _ignore_until_end_command,
}

# Ensure at least this regex is compiled.
_command_pattern = re.compile(fr'(?P<indent>\s*){OP}(?P<command>[a-zA-Z]+)(?P<rest>.*)')

def _convert(lines, app=None):
    handler = _plain(app=app)

    for line in lines:
        if line.strip() == '' and handler.blank_line_ends():
            handler = _plain(app=app)
            yield from handler.convert(line)
            continue

        mo = _command_pattern.match(line)
        if mo is None:
            # No command match, continue with current handler
            yield from handler.convert(line)
            continue

        command = mo.group('command')

        handler_cls = _handlers.get(command)
        if handler_cls is None:
            # Unknown command, continue with current handler
            yield from handler.convert(line)
            continue

        if not handler.command_ends(command):
            # Command does not finish block, continue with current handler
            yield from handler.convert(line)
            continue

        # Switch paragraph handler, and emit header for it
        handler = handler_cls(app=app, **mo.groupdict())

        yield from handler.header()

def _process_docstring(app, lines, transform, options):
    if transform != app.config.hawkmoth_javadoc_transform:
        return

    lines[:] = [line for line in _convert(app=app, lines=lines)]

def process_docstring(lines):
    """Simple interface for CLI and testing."""
    lines[:] = [line for line in _convert(lines=lines)]

def setup(app):
    app.setup_extension('hawkmoth')

    app.add_config_value('hawkmoth_javadoc_transform', 'javadoc', 'env', [str])

    app.connect('hawkmoth-process-docstring', _process_docstring)

    return {
        'parallel_read_safe': True,
    }
