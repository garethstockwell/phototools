"""
phototools.commands.metadata_google
"""

import json
import os
import pickle

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from phototools.commands.base import Command


class MetadataGoogle(Command):
    """
    Extract metadata from Google Photos, and report as JSON

    Based on code from https://medium.com/@najeem/analyzing-my-google-photos-library-with-python-and-pandas-bcb746c2d0f2
    """

    NAME = "metadata-google"

    @classmethod
    def init_parser(cls, parser):
        parser.add_argument(
            "credentials",
            metavar="CRED",
            help="path to credentials JSON file")

    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

    TOKEN = "metadata_google.pickle"

    def query(self):
        creds = None

        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.TOKEN):
            with open(self.TOKEN, 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.args.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.TOKEN, 'wb') as token:
                pickle.dump(creds, token)

        photos = build('photoslibrary', 'v1', credentials=creds)

        items = []
        nextpagetoken = None
        # The default number of media items to return at a time is 25.
        # The maximum pageSize is 100.
        while nextpagetoken != '':
            print(f"Number of items processed:{len(items)}", end='\r')
            results = photos.mediaItems().list(
                pageSize=100, pageToken=nextpagetoken).execute()
            items += results.get('mediaItems', [])
            nextpagetoken = results.get('nextPageToken', '')

        return items

    def _execute(self):
        data = self.query()
        self.output.write(json.dumps(data, indent=4))
