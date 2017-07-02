#!/usr/bin/env python3

import pathlib
import subprocess
import sys

def git_path(check=True):
    """
    locate git's root directory

    If `check` is True, the execution end if git root not found.
    Otherwise `None` is returned.
    """
    complete = subprocess.run(['git', 'rev-parse', '--show-toplevel'],
                              stdout=subprocess.PIPE, encoding='utf-8')
    if complete.returncode == 0:
        return pathlib.Path(complete.stdout[:-1])
    elif check:
        sys.exit(complete.returncode)
    else:
        return None

def file_location(file_name, check=True):
    """
    locate ancestor directory containing specified `file_name`

    If `check` is True, the execution end if git root not found.
    Otherwise `None` is returned.
    """
    current = pathlib.Path.cwd()
    while not (current / file_name).is_file():
        if len(current.parts) == 1:
            break
        current = current.parent
    if (current / file_name).is_file():
        return current
    elif check:
        print(f'expected file `{file_name}` not found')
        sys.exit(4)
    else:
        return None
