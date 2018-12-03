#!/usr/bin/env python3
"""
Create a new command from the template.

Subcommand name is expected to be dash separated lower-case
alpha-numeric.

Unless the `--no-edit` option selected, the command starts editor for
newly created file. Similar to `git`, it looks for `VISUAL` and `EDITOR`
environment variables, and falls back to `e` (whatever `e` is on your
PATH).
"""

import os
import pathlib
import re
import shlex
import string
import subprocess
import sys

import cmdutil


TEMPLATE = '''\
#!/usr/bin/env python3
"""
Brief description of the `subcommand-name`.

Additional information about `subcommand-name`.
"""

import sys

import cmdutil


class `SubcommandName`(cmdutil.Subcommand):

    # def configure_parser(self, parser):
    #     """configure parser with additional arguments"""
    #     parser.add_argument('foo',
    #                         help='positional foo.')
    #     parser.add_argument('-r', '--bar',
    #                         action='store_true',
    #                         help='parameter-less bar')

    # def validate_arguments(self):
    #     """
    #     Additional validation of parsed arguments in `self.arguments`.
    #
    #     It is expected to call `self.error()` on violations.
    #     """
    #     pass

    def execute(self):
        print(self.arguments)


if __name__ == "__main__":
    `SubcommandName`().run(sys.argv)
'''


class New(cmdutil.Subcommand):

    def configure_parser(self, parser):
        parser.add_argument('subcommand_name',
                            help='name of the subcommand.')
        parser.add_argument('-w', '--overwrite',
                            action='store_true',
                            help='overwrite subcommand if exists')
        parser.add_argument('-n', '--no-edit', action='store_true',
                            help='do not start editor for the subcommand')

    def validate_arguments(self):
        subcommand = self.arguments.subcommand_name
        if not re.match(r'[a-z0-9]+([-_][a-z0-9]+)*', subcommand):
            self.arguments_error(f'invalid subcommand name `{subcommand}`')
        subcommand_path = self._subcommand_path()
        if subcommand_path.is_file() and not self.arguments.overwrite:
            self.arguments_error(f'subcommand `{subcommand}` already exists. '
                                 'You can use `--overwrite` flag if desirable')


    def _load_template(self):
        template_path = pathlib.Path(pathlib.Path(__file__).parent, 'template')
        with template_path.open('r') as f:
            return f.read()

    @staticmethod
    def _split(value):
        return re.split(r'-|_', value)

    @staticmethod
    def _to_dash(tokens):
        return '-'.join(tokens)

    @staticmethod
    def _to_underscore(tokens):
        return '-'.join(tokens)

    @staticmethod
    def _to_camelcase(tokens):
        return ''.join(string.capwords(token) for token in tokens)

    def _replace_variables(self, text, variables):
        for name, value in variables.items():
            text = text.replace(f'`{name}`', f'{value}')
        return text

    def _subcommand_path(self):
        subcommand_tokens = self._split(self.arguments.subcommand_name)
        self_path = pathlib.Path(__file__)
        prefix = self._split(self_path.name)[0]
        name = self._to_dash([prefix] + subcommand_tokens)
        return pathlib.Path(self_path.parent, name + '.py')

    def _save_subcommand(self, path, text):
        with open(path, 'w') as f:
            f.write(text)

    def _start_editor(self, path):
        editor = os.getenv('VISUAL') or os.getenv('EDITOR') or 'e'
        editor_command = shlex.split(editor)
        editor_command.append(str(path))
        output = None if self.arguments.verbose else subprocess.DEVNULL
        subprocess.Popen(editor_command, stdout=output, stderr=output)

    def _build_variables(self):
        subcommand_tokens = self._split(self.arguments.subcommand_name)
        name_tokens = self._split('subcommand-name')
        return {
            self._to_dash(name_tokens): self._to_dash(subcommand_tokens),
            self._to_underscore(name_tokens): self._to_underscore(subcommand_tokens),
            self._to_camelcase(name_tokens): self._to_camelcase(subcommand_tokens),
        }

    def execute(self):
        variables = self._build_variables()
        text = self._replace_variables(TEMPLATE, variables)
        subcommand_path = self._subcommand_path()
        self._save_subcommand(subcommand_path, text)
        subcommand_path.chmod(0o777)
        if not self.arguments.no_edit:
            self._start_editor(subcommand_path)


if __name__ == '__main__':
    New().run(sys.argv)
