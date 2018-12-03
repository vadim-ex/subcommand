#!/usr/bin/env python3

import pathlib
import subprocess
import sys

def _exec(command, check):
    """
    execute the `command`.

    If `check` is True, the execution end if git root not found.
    Otherwise `None` is returned.
    """
    complete = subprocess.run(command, stdout=subprocess.PIPE, encoding='utf-8')
    if complete.returncode == 0:
        return complete.stdout[:-1]
    elif check:
        sys.exit(complete.returncode)
    else:
        return None

def git_path(check=True):
    """
    locate git's root directory

    If `check` is True, the execution end if git root not found.
    Otherwise `None` is returned.
    """
    path = _exec('git rev-parse --show-toplevel'.split(), check)
    return pathlib.Path(path) if path else path

def git_ref(check=True):
    """
    return name for current branch / tag

    If `check` is True, the execution end if git root not found.
    Otherwise `None` is returned.
    """
    branch = _exec('git rev-parse --abbrev-ref HEAD'.split(), check)
    if branch != 'HEAD':
        return branch
    tag_ref = _exec('git describe --all'.split(), check)
    return tag_ref[5:] if tag_ref.startswith('tags/') else 'HEAD'

def git_sha(check=True):
    """
    return sha of current commit

    If `check` is True, the execution end if git root not found.
    Otherwise `None` is returned.
    """
    return _exec('git rev-parse HEAD'.split(), check)


def git_dirty(check=True):
    """
    returns dirty status of git
    """
    command = 'git diff-index --quiet HEAD --'.split()
    complete = subprocess.run(command, stdout=subprocess.PIPE, encoding='utf-8')
    return_code = complete.returncode
    if return_code == 0:
        return False
    elif return_code == 1:
        return True
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

def project_location(file_name, check=True):
    """
    Locate a minimal directory containing specified `file_name`

    If `check` is True, the execution end if git root not found.
    Otherwise `None` is returned.
    """
    current = pathlib.Path.cwd()
    projects = current.glob('**/' + file_name)
    while not list(projects) and len(current.parts) > 1:
        current = current.parent
        projects = current.glob('**/' + file_name)
    if projects:
        return current
    elif check:
        print(f'expected file `{file_name}` not found')
        sys.exit(4)
    else:
        return None
