from __future__ import print_function

import json
import logging
from typing import List

from googleapiclient.errors import HttpError

from car_researcher.collate.sheets import auth_sheets_service, load_config, \
    append_search_flat_objects
from car_researcher.scrape.kbb_search import VEHICLE_DETAILS_REGEX


def parse_listings_dir(path: str) -> List[dict]:
    with open(f'{path}/index.txt') as urls_file:
        listing_ids = [VEHICLE_DETAILS_REGEX.search(url.strip())[1] for url in urls_file.readlines()]
    listings = []
    for listing_id in listing_ids:
        file_path = f'{path}/{listing_id}.json'
        try:
            with open(file_path) as json_file:
                listings.append(json.load(json_file))
        except Exception as e:
            logging.warning(f'Failed to parse: {file_path}')
            print(e)
    return listings


def flatten_kbb_listing(listing: dict) -> dict:
    vehicle_features = {}
    for entry in listing['vehicle_features']:
        prefix = entry['name']
        features = ''.join([f'{f}\n' for f in entry['features']])
        vehicle_features[f'vehicle_features.{prefix}'] = features

    return {
        "url": listing['url'],
        "miles": listing['miles'],
        "engine_description": listing['engine_description'],
        "mpg.city": listing['mpg']['city'],
        "mpg.highway": listing['mpg']['highway'],
        "drive_type": listing['drive_type'],
        "transmission": listing['transmission'],
        **vehicle_features
    }


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    import argparse
    parser = argparse.ArgumentParser(
        prog='scrape_kbb_listing',
        description='Appends the listing to Google Sheets',
        epilog='Use --help for more info')
    parser.add_argument('--config', help="JSON file containing details of the target spreadsheet")
    parser.add_argument('input', help="Directory containing the scraped listing JSONs and index.txt file")

    args = parser.parse_args()

    ranges = load_config(args.config)
    listings = parse_listings_dir(args.input)
    listings = [flatten_kbb_listing(listing) for listing in listings]

    try:
        service = auth_sheets_service()

        # Call the Sheets API
        sheet = service.spreadsheets()
        append_search_flat_objects(sheet, ranges['listing_headers'], ranges['listing_data'], listings)

    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
