"""
phototools.commands.base
"""

import argparse
import sys

class Command:
    """
    Base class for commands
    """

    @classmethod
    def register(cls, parser):
        """
        Register a command with the parser
        """
        subparser = parser.add_parser(cls.NAME, help=cls.__doc__)
        cls.init_parser(subparser)
        subparser.add_argument(
            "-o", "--output",
            metavar="PATH",
            help="output path")
        subparser.set_defaults(cls=cls)

    def __init__(self, args):
        self.args = args

    def execute(self):
        self.output = sys.stdout
        if self.args.output:
            self.output = open(self.args.output, "wt")

        self._execute()