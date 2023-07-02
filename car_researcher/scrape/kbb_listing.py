import re
from dataclasses import dataclass
from typing import List

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from car_researcher.scrape.fetch import Fetcher, RequestsHtmlFetcher
from car_researcher.scrape.scrape_utils import assert_unique, parse_int, remove_redundant_whitespace

MILES_REGEX = re.compile('([0-9,]+) miles')
MPG_REGEX = re.compile('([0-9]+) City / ([0-9]+) Highway')


@dataclass
class Mileage:
    city: int
    highway: int


@dataclass
class VehicleFeature:
    name: str
    features: List[str]


@dataclass
class KBBListing:
    miles: int
    engine_description: str
    mpg: Mileage
    drive_type: str
    transmission: str
    vehicle_features: List[VehicleFeature]


def scrape_kbb_listing(url: str, fetcher: Fetcher):
    html = fetcher.proxy_get(url, (By.XPATH, '//a[@data-cmp="ownerWebsiteCTA"]'))

    miles = MILES_REGEX.match(scrape_icon_field(html, 'MILEAGE'))[1]
    miles = parse_int(miles)

    engine_description = scrape_icon_field(html, 'ENGINE_DESCRIPTION')

    mpg_text = scrape_icon_field(html, 'MPG')
    mpg_text = remove_redundant_whitespace(mpg_text)
    mpg_city, mpg_hwy = MPG_REGEX.match(mpg_text).groups()
    mpg = Mileage(int(mpg_city), int(mpg_hwy))

    transmission = scrape_icon_field(html, 'TRANSMISSION')
    drive_type = scrape_icon_field(html, 'DRIVE TYPE')

    features = scrape_features_accordions(html)
    features = [VehicleFeature(name, feats) for name, feats in features]

    return KBBListing(miles=miles,
                      engine_description=engine_description,
                      mpg=mpg, drive_type=drive_type, transmission=transmission, vehicle_features=features)


def scrape_icon_field(html: BeautifulSoup, aria_label):
    miles_icon = assert_unique(html.find_all('div', attrs={'aria-label': aria_label}))
    for sib in miles_icon.parent.next_siblings:
        if sib.name == 'div' and sib.attrs['class'] == ['col-xs-10', 'margin-bottom-0']:
            raw_text = sib.string or next(sib.stripped_strings)
            return remove_redundant_whitespace(raw_text)
    raise AssertionError(f"Icon field siblings don't match: {list(miles_icon.parent.next_siblings)}")


def scrape_features_accordions(html: BeautifulSoup):
    extracted_data = []
    accordions = html.find_all('div', 'accordion-panel')
    for accordion in accordions:
        title = remove_redundant_whitespace(accordion.findChild('span', 'text-size-400').string)
        features = [remove_redundant_whitespace(li.string) for li in accordion.findChildren('li')]
        extracted_data.append((title, features))
    return extracted_data


def main():
    import argparse
    parser = argparse.ArgumentParser(
        prog='scrape_kbb_listing',
        description='Scrapes the key information from a KBB listing',
        epilog='Use --help for more info')
    parser.add_argument('url', help="The KBB listing url to scrape")

    args = parser.parse_args()
    listing = scrape_kbb_listing(args.url, RequestsHtmlFetcher())
    print(listing)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
