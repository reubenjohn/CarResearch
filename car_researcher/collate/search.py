from __future__ import print_function

import json

from googleapiclient.errors import HttpError

from car_researcher.collate.sheets import auth_sheets_service, append_search_flat_objects, load_config


def main():
    import argparse
    parser = argparse.ArgumentParser(
        prog='append_search_results',
        description='Appends search results to Google Sheets',
        epilog='Use --help for more info')
    parser.add_argument('--config', help="JSON file containing details of the target spreadsheet")
    parser.add_argument('data', help="JSON file containing the data to be appended")

    args = parser.parse_args()

    ranges = load_config(args.config)
    with open(args.data) as data_file:
        data = json.load(data_file)

    try:
        service = auth_sheets_service()

        # Call the Sheets API
        sheet = service.spreadsheets()
        append_search_flat_objects(sheet, ranges['search_result_headers'], ranges['search_result_data'], data)

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
