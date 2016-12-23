#!/usr/bin/env python3
"""
Print table of colors and their ANSI codes.

See also https://en.wikipedia.org/wiki/ANSI_escape_code
"""

import sys

import cmdutil


class Colors(cmdutil.Subcommand):
    def execute(self):
        e = '\x1B'
        r = f'{e}[0m'
        print('Color code : `\\x1B[‹dd›m` for regular colors, and')
        print('             `\\x1B[‹dd›;1m` for bright ones.')
        print('Codes can be combined with `;`, eg `\\x1B[30;47m`.')
        print("Bash control: `echo -e '\e[32;1mMerry \e[37;1mChris\e[31;1mtmas!\e[0m'`")
        print()
        for color in range(30, 38):
            other = 37 if color == 30 else 30
            colors = [
                f'{color:2d}: {e}[{color};{other + 10}mXXX{r}',
                f'{color:2d};1: {e}[{color};1mXXX{r}',
                f'{color + 10:2d}: {e}[{other};{color + 10}mXXX{r}',
            ]
            print(' ', '    '.join(colors))


if __name__ == "__main__":
    Colors().run(sys.argv)
