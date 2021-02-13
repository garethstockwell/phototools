# phototools

This repository contains tools for checking whether all of a set of local photos are present in a Google Photos library.

## How to use

1. Extract EXIF metadata from local files

    phototools metadata-local some-local-path -o local.json

2. Extract metadata from Google Photos

    phototools metadata-google credentials.json -o google.json

The credentials.json file contains an OAuth token which gives access to the target Google Photos library.
For details of how to set this up, see https://medium.com/@najeem/analyzing-my-google-photos-library-with-python-and-pandas-bcb746c2d0f2

3. Compare the two libraries

    phototools check local.json google.json

The comparison is done based on the creation time of each photo.
The output contains a line for each of the following cases:

    ?local <timestamp>
        More than one local photo had the same creation time

    ?google <timestamp>
        More that one Google photo had a creation time which matched a local photo

    - <timestamp>
        The timestamp of a local photo was not found in the Google Photos library

## Author

Gareth Stockwell <gareth.stockwell@gmail.com>
