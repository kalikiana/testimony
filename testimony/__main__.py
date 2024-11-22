# SPDX-FileCopyrightText: 2024 Liv Dywan <liv.dywan@suse.com>
#
# SPDX-License-Identifier: EUPL-1.2

"""Main entry point for the module"""
from . import cli

def __main__():
    cli.CLI().run()
