#!/usr/bin/env python3
"""
Main command to delegate to subcommands.

It does delegation and help, nothing more.
"""

import pathlib
import sys


LIB_DIR = 'cmd-lib'


lib_path = pathlib.Path(pathlib.Path(sys.argv[0]).parent, LIB_DIR)
sys.path.insert(0, str(lib_path))
import cmdutil
cmdutil.Command(sys.argv[0], __doc__, lib_path).run(sys.argv)
