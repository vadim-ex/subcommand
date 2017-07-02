#!/usr/bin/env python3
"""
Base class for subcommands.
"""

import argparse
import sys


class Subcommand(object):
    """
    Base class for subcommand.
    """

    def _description(self):
        description = self.module.__doc__ or ''
        if not description.strip():
            description = self.__doc__ or ''
        lines = description.split('\n')
        indent = len(description) + 1
        for line in lines:
            stripped_line = line.lstrip()
            line_indent = len(line) - len(stripped_line)
            if stripped_line and line_indent < indent:
                indent = line_indent
        return ('\n'.join(line[indent:] for line in lines)).strip()

    def _create_parser(self, subcommand=None):
        parser_config = {
            'description': self._description(),
            'formatter_class': argparse.RawTextHelpFormatter,
            'allow_abbrev': False,
            'add_help': False,
        }
        if subcommand:
            parser = argparse.ArgumentParser()                     \
                .add_subparsers()                                  \
                .add_parser(subcommand, **parser_config)
        else:
            parser = argparse.ArgumentParser(**parser_config)

        parser.unknown_args_name = None
        return parser

    def configure_parser(self, parser):
        return parser

    def _configure_parser(self, parser):
        parser = self.configure_parser(parser) or parser
        parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
        parser.add_argument('-h', '-?', '--help', action='help', help='show this help message and exit')
        return parser

    def _parse(self, args, subcommand):
        parser = self._create_parser(subcommand)
        self.parser = self._configure_parser(parser)
        self.args = args[(2 if subcommand else 1):]
        unknown_args_name = getattr(self.parser, 'unknown_args_name', None)
        if unknown_args_name:
            parsed, unknown = self.parser.parse_known_args(self.args)
            setattr(parsed, unknown_args_name, unknown)
        else:
            parsed = self.parser.parse_args(self.args)
        return parsed

    def arguments_error(self, message):
        self.parser.print_usage()
        self.error(message, returncode=2)

    def error(self, message, returncode=4):
        print(message)
        sys.exit(returncode)

    def validate_arguments(self):
        pass

    def run(self, args, subcommand=None):
        """entry point of the module (required callback)"""
        self.module = sys.modules[self.__class__.__module__]
        self.arguments = self._parse(args, subcommand)
        self.validate_arguments()
        sys.exit(self.execute() or 0)


if __name__ == '__main__':
    pass
