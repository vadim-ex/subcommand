#!/usr/bin/env python3
"""
Edit subcommand.

Choice of editor: similar to `git`, it looks for `VISUAL` and `EDITOR`
environment variables, and falls back to `e` (whatever `e` is on your
PATH).
"""

import os
import pathlib
import re
import shlex
import subprocess
import sys

import cmdutil


class Edit(cmdutil.Subcommand):

    def configure_parser(self, parser):
        parser.add_argument('subcommand_name',
                            help='name of the subcommand.')

    def _subcommand_path(self, subcommand_name):
        subcommand_tokens = re.split(r'-|_', subcommand_name)
        self_path = pathlib.Path(__file__)
        prefix = re.split(r'-|_', self_path.name)[0]
        name = '-'.join([prefix] + subcommand_tokens)
        return pathlib.Path(self_path.parent, name + '.py')

    def validate_arguments(self):
        subcommand_name = self.arguments.subcommand_name
        subcommand_path = self._subcommand_path(subcommand_name)
        if not subcommand_path.is_file():
            self.error(f'command not found: `{subcommand_name}`')

    def _start_editor(self, path):
        editor = os.getenv('VISUAL') or os.getenv('EDITOR') or 'e'
        editor_command = shlex.split(editor)
        editor_command.append(str(path))
        output = None if self.arguments.verbose else subprocess.DEVNULL
        subprocess.Popen(editor_command, stdout=output, stderr=output)

    def execute(self):
        self._start_editor(self._subcommand_path(self.arguments.subcommand_name))


if __name__ == "__main__":
    Edit().run(sys.argv)
