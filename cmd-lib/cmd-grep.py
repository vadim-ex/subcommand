#!/usr/bin/env python3
"""
Run grep, ignoring irrelevant dirs.

Note on parameters:
* it is easier to control colors using command's option
* if switches need to be passed to grep, one can use `--`
"""

import argparse
import subprocess
import sys

import cmdutil

EXCLUDED_DIRS = [".git", ".idea"]


class Grep(cmdutil.Subcommand):
    def configure_parser(self, parser):
        parser.add_argument(
            "-c",
            "--color",
            "--colour",
            choices=["a", "always", "n", "never"],
            default=None,
            help="use ANSI colors in output",
        )
        parser.add_argument(
            "-g",
            "--grep",
            action="store_true",
            help="use grep directly (instead of git grep)",
        )
        parser.add_argument(
            "-p", "--pager", action="store_true", help="enable paging of results"
        )
        parser.unknown_args_name = "grep_args"

    def execute(self):
        arguments = self.arguments
        if arguments.verbose:
            print("grep args:", arguments.grep_args, flush=True)
        if arguments.grep:
            command = ["grep", "-r"]
        else:
            command = ["git"]
            if not arguments.pager:
                command.append("--no-pager")
            command.append("grep")
        if arguments.color:
            if arguments.color[:1] == "a":
                command.append("--color=always")
            if arguments.color[:1] == "n":
                command.append("--color=never")
        else:
            command.append("--color=auto")
        command += arguments.grep_args
        if arguments.grep:
            command += [f"--exclude-dir={dir}" for dir in EXCLUDED_DIRS]
        completed_process = subprocess.run(command)
        return completed_process.returncode


if __name__ == "__main__":
    Grep().run(sys.argv)
