import re
from dataclasses import dataclass

from car_researcher.scrape.fetch import Fetcher, RequestsHtmlFetcher
from car_researcher.scrape.scrape_utils import assert_unique, first_non_none, parse_int

MILES_REGEX = re.compile('([0-9,]+) miles')


@dataclass
class KBBListing:
    miles: int


def scrape_kbb_listing(url: str, fetcher: Fetcher):
    html = fetcher.get(url)
    miles_icon = assert_unique(html.find_all('div', attrs={'aria-label': 'MILEAGE'}))
    miles = first_non_none(MILES_REGEX.match(sib.string) for sib in miles_icon.parent.next_siblings)[1]
    miles = parse_int(miles)
    return KBBListing(miles)


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
