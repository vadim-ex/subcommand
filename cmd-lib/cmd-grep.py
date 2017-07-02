#!/usr/bin/env python3
"""
Run grep, ignoring irrelevant dirs.

All unrecognized options are passed to grep.
"""

import argparse
import subprocess
import sys

import cmdutil

EXCLUDED_DIRS = [
    '.git',
    '.idea',
]

class Grep(cmdutil.Subcommand):
    def configure_parser(self, parser):
        parser.add_argument('-c', '--color', '--colour',
            choices=['a', 'always', 'n', 'never'], default=None,
            help='use ANSI colors in output')
        parser.unknown_args_name = 'grep_args'

    def execute(self):
        arguments = self.arguments
        if arguments.verbose:
            print('grep args:', arguments.grep_args, flush=True)
        command = ['grep', '-r']
        if arguments.color:
            if arguments.color[:1] == 'a':
                command.append('--color=always')
            if arguments.color[:1] == 'n':
                command.append('--color=never')
        else:
            command.append('--color=auto')
        command += arguments.grep_args + [f'--exclude-dir={dir}' for dir in EXCLUDED_DIRS]
        completed_process = subprocess.run(command)
        return completed_process.returncode


if __name__ == "__main__":
    Grep().run(sys.argv)
