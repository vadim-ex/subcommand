![Status: Incubating](https://img.shields.io/badge/status-incubating-blue.svg?style=flat)
![Open Source: Yes](https://img.shields.io/badge/open_source-MIT-green.svg?style=flat)

Command / Subcommand Utility
============================

The utility simplifies creation of the `git` style commands. It provides
umbrella command `cmd` (it can be renamed as desirable), and a library
module to create subcommands.

_License_: [MIT License](https://github.com/vadim-ex/subcommand/blob/master/license)

_Language_: Python 3.6+

_Version_: 0.1.0


Build Your Own Command (Getting Started)
========================================

It is easy!

(I will use `target` as an example for target command name.)

1. Copy source files into appropriate location.

2. Rename appropriately:

    2.1. Rename `cmd` script to `target` and `cmd-lib` to `target-lib`.
    (OK, any suitable name actually. It could be `foobar`, or `barfoo`,
    as long as you update `LIB_DIR` correctly -- see below.)

    **Warning:** do **not** rename `target-lib/cmdutil` (unless you want
    to correct all its occurrences in the code).

    2.2. Rename commands, for example `target-lib/cmd-new` to
    `target-lib/target-new`.

3. Update `target`:

    3.1. Edit your command description (the `target` module's
    docstring).

    3.2. Edit `LIB_DIR` to match your `target-lib` name.

4. Update `path` to include `target`, or create softlink to the `target`
in the directory on path.

5. Create a subcommand:

    5.1. Run `target new my-command`. To be sure, `new` is a regular
    subcommand, and is an example of how subcommand can be implemented.

    5.2. Edit description (`target-lib/target-my-command.py` docstring).

    5.3. Edit subcommand's `execute()` method (by default, it prints
    arguments).

6. Try it!

    6.1. Run `target` with no parameters. It should print list of
    subcommands with their first line of descriptions.

    6.2. Run `target my-subcommand --help`. It should print detailed
    description of the subcommand and its command line arguments.

7. Create an alias for the command:

    7.1. Create a softlink:
       ```bash
       ln -s target-my-command.py target-lib/target-mc.py
       ```

    7.2. Done!

