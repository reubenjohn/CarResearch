from __future__ import print_function

import json
import os.path
from dataclasses import dataclass
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and srange of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'


@dataclass
class SheetRange:
    id: str
    range: str


class SheetManip:
    def __init__(self, sheet, spreadsheet_id: str):
        self.sheet = sheet
        self.spreadsheet_id = spreadsheet_id


def read_headers(sheet, srange: SheetRange) -> List[str]:
    result = sheet.values().get(spreadsheetId=srange.id, range=srange.range).execute()
    values = result.get('values', [])
    return values[0]


def load_config(path: str):
    with open(path) as fp:
        d = json.load(fp)
        data_locations = {key: SheetRange(**val['sheet_range']) for key, val in d['data_locations'].items() if
                          val['storage'] == 'google-sheets'}
        return data_locations


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    ranges = load_config('config/collate.json')
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('creds/token.json'):
        creds = Credentials.from_authorized_user_file('creds/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'creds/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('creds/token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        print(read_headers(sheet, ranges['search_results']))

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
