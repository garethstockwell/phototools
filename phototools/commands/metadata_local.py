"""
phototools.commands.metadata_local
"""

from json import JSONEncoder
import json
import os
import sys

from PIL.ExifTags import TAGS
from PIL.TiffImagePlugin import IFDRational
from PIL import Image

from phototools.commands.base import Command


class Encoder(JSONEncoder):
    """
    Helper class to ensure all EXIF values are JSON serializable
    """

    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode("utf-8", errors="replace")
        if isinstance(obj, IFDRational):
            try:
                return obj.numerator / obj.denominator
            except:
                return None
        else:
            return json.JSONEncoder.default(self, obj)


class MetadataLocal(Command):
    """
    Extract metadata from photos on local filesystem, and report as JSON
    """

    NAME = "metadata-local"

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
                try:
                    image = Image.open(path)
                    exif = image.getexif()
                    item = {TAGS.get(key): val for key, val in exif.items()}
                    item['path'] = path
                    data.append(item)
                except:
                    sys.stderr.write('Skipping {}\n'.format(path))

        self.output.write(json.dumps(data, indent=4, sort_keys=True, cls=Encoder))
