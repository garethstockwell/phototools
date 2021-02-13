"""
phototools.commands.check
"""

import json

from phototools.commands.base import Command


def process(data, key_func):
    """
    Convert list of items into a dictionary, keyed by creation time

    key_func is a callable which generates the key (creation time) for each item
    """

    result = {
        "duplicate_keys": set(),
        "items": dict()
    }
    for item in data:
        key = key_func(item)
        if key in result["items"]:
            result["duplicate_keys"].add(key)
        else:
            result["items"][key] = item
    return result


def local_time(value):
    """
    Convert EXIF timestamp into a canonical format
    """

    date, time = value.split(" ")
    return date.replace(":", "-") + " " + time


def google_time(value):
    """
    Convert Google timestamp into a canonical format
    """

    value = value.replace("Z", "")
    return value.replace("T", " ")


class Check(Command):
    """
    Check that all files in local folder are present in Google Photos library
    """

    NAME = "check"

    @classmethod
    def init_parser(cls, parser):
        parser.add_argument(
            "local",
            metavar="PATH",
            help="path to JSON file for local photos")
        parser.add_argument(
            "google",
            metavar="PATH",
            help="path to JSON file for Google photos")

    def _execute(self):
        with open(self.args.local) as stream:
            data = json.load(stream)
            local = process(data, lambda item: local_time(item["DateTimeOriginal"]))

        for key in local["duplicate_keys"]:
            self.output.write("?local " + key + "\n")

        with open(self.args.google) as stream:
            data = json.load(stream)
            google = process(data,
                lambda item: google_time(item["mediaMetadata"]["creationTime"]))

        for key in local["items"]:
            if key in google["duplicate_keys"]:
                self.output.write("?google " + key + "\n")
            elif not key in google["items"]:
                self.output.write("- " + key + "\n")
