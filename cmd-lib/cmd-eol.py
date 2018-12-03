#!/usr/bin/env python3
"""
Converts eols to desirable os standard.

The command supports both direct filenames and glob templates. It also translates directories into template for their content.
"""

import glob
import os
import sys

import cmdutil


class Eol(cmdutil.Subcommand):
    def configure_parser(self, parser):
        parser.add_argument("filenames", nargs="+", help="files to convert")
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            "-u",
            "--unix",
            action="store_true",
            default=False,
            help="convert to unix (default, LF)",
        )
        group.add_argument(
            "-d",
            "--dos",
            action="store_true",
            default=False,
            help="convert to dos (CR-LF)",
        )
        group.add_argument(
            "-m",
            "--mac",
            action="store_true",
            default=False,
            help="convert to mac (CR)",
        )
        group.add_argument(
            "-s",
            "--stats",
            action="store_true",
            default=False,
            help="print statistics about used eols",
        )

    def generate_paths(self, filenames):
        paths = set()
        for filename in filenames:

            if os.path.isdir(filename):
                pattern = os.path.join(filename, "*")
            else:
                pattern = filename
            paths.update(glob.glob(pattern, recursive=True))
        return sorted(p for p in paths if not os.path.isdir(p))

    def stat_path(self, path):
        with open(path, "rb") as f:
            text = f.read()
        nix = 0
        mac = 0
        dos = 0
        cr = False
        for byte in text:
            if cr:
                if byte == 0x0A:
                    dos += 1
                else:
                    mac += 1
            else:
                if byte == 0x0A:
                    nix += 1
            cr = byte == 0x0D
        if cr:
            mac += 1
        return (nix, mac, dos)

    def process(self, path, separator):
        with open(path, "rb") as f:
            text = f.read()

        out_text = text.replace(b"\r\n", b"\n")
        out_text = out_text.replace(b"\r", b"\n")
        if separator != b"\n":
            out_text = out_text.replace(b"\n", separator)

        if text == out_text:
            return

        with open(path, "wb") as f:
            f.write(out_text)

    def execute(self):
        arguments = self.arguments
        paths = self.generate_paths(arguments.filenames)
        if arguments.stats:
            print("   nix    mac    dos    path")
            print("-" * 32)
            n = 0
            m = 0
            d = 0
            files = 0
            for path in paths:
                nix, mac, dos = self.stat_path(path)
                print(f"{nix: 6d} {mac: 6d} {dos: 6d}  {path}")
                n += nix
                m += mac
                d += dos
                files += 1
            print("-" * 32)
            print(f"{n: 6d} {m: 6d} {d: 6d}  total in {files} files")
        else:
            if arguments.mac:
                separator = b"\r"
            elif arguments.dos:
                separator = b"\r\n"
            else:
                separator = b"\n"
            for path in paths:
                self.process(path, separator)


if __name__ == "__main__":
    Eol().run(sys.argv)
