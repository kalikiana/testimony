# SPDX-FileCopyrightText: 2024 Liv Dywan <liv.dywan@suse.com>
#
# SPDX-License-Identifier: EUPL-1.2

"""Processing of command-line interactions"""
import argparse
from . import model


class CLI:
    """Parse arguments given on the CLI"""

    args: argparse.ArgumentParser

    def __init__(self):
        self.parse()

    def parse(self, args=None) -> None:
        """Setup up parsing with optional input override"""
        parser = argparse.ArgumentParser(description="Make sense of openQA results")
        parser.add_argument("jobs", type=str, nargs='+', help='openQA jobs')
        self.args = parser.parse_args(args)

    def run(self) -> None:
        """Provide a main entry point"""
        return model.Model(self.args.jobs).train()
