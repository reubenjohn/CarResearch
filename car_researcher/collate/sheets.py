from __future__ import print_function

import json
import logging
import os
from dataclasses import dataclass
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


@dataclass
class SheetRange:
    id: str
    range: str


def load_config(path: str):
    with open(path) as fp:
        d = json.load(fp)
        data_locations = {key: SheetRange(**val['sheet_range']) for key, val in d['data_locations'].items() if
                          val['storage'] == 'google-sheets'}
        return data_locations


def auth_sheets_service():
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
    service = build('sheets', 'v4', credentials=creds)
    return service


def fetch_headers(sheet, srange: SheetRange) -> List[str]:
    result = sheet.values().get(spreadsheetId=srange.id, range=srange.range).execute()
    values = result.get('values', [])
    return values[0]


def flat_objects_to_rows(headers: List[str], objects: List[dict]):
    objects_keys = set()
    values = []
    for obj in objects:
        objects_keys.union(obj.keys())
        values.append([obj[k] if k in obj else '' for k in headers])

    extraneous = objects_keys.difference(headers)
    if extraneous:
        logging.warning(f"Extraneous objects_keys found in objects to append: {extraneous}")

    return values


def append_search_flat_objects(sheet, headers_range: SheetRange, data_range: SheetRange, objects: List[dict]):
    headers = fetch_headers(sheet, headers_range)
    values = flat_objects_to_rows(headers, objects)
    sheet.values().append(spreadsheetId=data_range.id, range=data_range.range, valueInputOption="RAW",
                          body={'values': values}).execute()
