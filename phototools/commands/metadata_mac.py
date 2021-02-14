"""
phototools.commands.metadata_mac
"""

from json import JSONEncoder
import json
import os
from subprocess import check_output
import sys


from phototools.commands.base import Command


class MetadataMac(Command):
    """
    Extract metadata from photos on local Mac filesystem, and report as JSON
    """

    NAME = "metadata-mac"

    @classmethod
    def init_parser(cls, parser):
        parser.add_argument(
            "path",
            metavar="PATH",
            help="path to directory to be scanned")

    def _execute(self):
        data = []
        for root, dnames, fnames in os.walk(self.args.path):
            for fname in fnames:
                path = os.path.join(root, fname)
                output = check_output(['mdls', path])
                for line in output.decode('utf-8').split('\n'):
                    if line.startswith('kMDItemContentCreationDate'):
                        tokens = line.split('=')
                        item = {
                            'path': path,
                            'DateTimeOriginal': tokens[1].strip(),
                        }
                        data.append(item)

        self.output.write(json.dumps(data, indent=4))
