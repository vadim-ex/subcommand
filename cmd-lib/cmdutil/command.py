#!/usr/bin/env python3
"""
Utility class for executing command.
"""

import collections
import importlib.util
import pathlib
import sys

from .subcommand import Subcommand


class Command(object):
    def __init__(self, command_string, description, lib_path):
        self.command = pathlib.Path(command_string)
        self.description = description
        self.lib_path = lib_path
        self.subcommands = None

    def _get_subcommand_module(self, path, subcommand):
        module_name = f'subcommand.{subcommand}'
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module

    def _get_subcommand_class(self, module):
        for subcommand_class in vars(module).values():
            if isinstance(subcommand_class, type) and issubclass(subcommand_class, Subcommand):
                return subcommand_class
        return None

    def _get_subcommand_description(self, path, subcommand):
        module = self._get_subcommand_module(path, subcommand)
        description = (module.__doc__ or '').strip()
        if not description:
            subcommand_class = self._get_subcommand_class(module)
            description = (subcommand_class.__doc__ or '').strip()
        return description.split('\n', 1)[0].strip()

    def _subcommand_prefix(self):
        return f'{self.command.stem}-'

    def _subcommand_list(self):
        clusters = collections.defaultdict(list)
        for subcommand, path in sorted(self.subcommands.items()):
            resolved_path = path.resolve()
            priority = -10**10 if not path.is_symlink() else -len(subcommand)
            clusters[resolved_path].append((priority, subcommand, path))
        subcommand_list = []
        for cluster in clusters.values():
            cluster = sorted(cluster)
            _, subcommand, path = cluster.pop(0)
            aliases = sorted(subcommand for _, subcommand, _ in cluster)
            subcommand_list.append((subcommand, aliases, path))
        return sorted(subcommand_list)

    def _command_help(self):
        print(f'usage: {self.command.name} subcommand ...\n')
        print(self.description.strip() + '\n')
        print('available subcommands:')
        for subcommand, aliases, path in self._subcommand_list():
            subcommand_description = self._get_subcommand_description(path, subcommand)
            names = subcommand
            if aliases:
                names += f' ({", ".join(sorted(aliases))})'
            column_width = 8
            if len(names) <= column_width:
                print(' ', names.ljust(column_width), subcommand_description)
            else:
                print(' ', names)
                print(''.ljust(column_width + 2), subcommand_description)
        print(f'\nRun `{self.command.name} ‹subcommand› --help` for more information.')

    def _discover_subcommands(self):
        prefix = self._subcommand_prefix()
        for path in self.lib_path.glob(f'{prefix}*.py'):
            yield path.stem[len(prefix):], path

    def _instantiate_subcommand(self, subcommand):
        module = self._get_subcommand_module(self.subcommands[subcommand], subcommand)
        subcommand_class = self._get_subcommand_class(module)
        return subcommand_class() if subcommand_class else None

    def _error(self, *message):
        for line in message:
            print(line)
        sys.exit(1)

    def run(self, args):
        self.subcommands = dict(self._discover_subcommands())
        if len(args) < 2 or args[1] in ['-h', '-?', '--help']:
            self._command_help()
            sys.exit(0)
        subcommand = args[1]
        path = self.subcommands.get(subcommand)
        if not path:
            self._error(f'Unknown subcommand `{subcommand}`',
                f'Run `{self.command.name} --help` for list of available subcommands.')
        instance = self._instantiate_subcommand(subcommand)
        if not instance:
            self._error(f'Cannot instantiate subcommand `{subcommand}`',
                'Did you forget to derive the class from Subcommand?')
        sys.exit(instance.run(args, subcommand=subcommand))


if __name__ == '__main__':
    pass
