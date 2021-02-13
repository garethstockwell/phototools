#!/usr/bin/env python3

"""
phototools.__main__
"""

import argparse
import sys

from phototools.commands.check import Check
from phototools.commands.metadata_google import MetadataGoogle
from phototools.commands.metadata_local import MetadataLocal

def main(args=None):

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    Check.register(subparsers)
    MetadataGoogle.register(subparsers)
    MetadataLocal.register(subparsers)

    args = parser.parse_args()

    # Execute selected command, or print help
    if "cls" in args.__dict__:
        command = args.cls(args)
        command.execute()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':

    sys.exit(main())
