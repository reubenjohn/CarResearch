import re
from dataclasses import dataclass

from car_researcher.scrape.fetch import Fetcher, RequestsHtmlFetcher
from car_researcher.scrape.scrape_utils import assert_unique, parse_int, remove_redundant_whitespace

MILES_REGEX = re.compile('([0-9,]+) miles')
MPG_REGEX = re.compile('([0-9]+) City / ([0-9]+) Highway')
WHITESPACE = re.compile('\s+')


@dataclass
class Mileage:
    city: int
    highway: int


@dataclass
class KBBListing:
    miles: int
    engine_description: str
    mpg: Mileage


def scrape_kbb_listing(url: str, fetcher: Fetcher):
    html = fetcher.get(url)

    miles = MILES_REGEX.match(scrape_icon_field(html, 'MILEAGE'))[1]
    miles = parse_int(miles)

    mpg_text = scrape_icon_field(html, 'MPG').replace('\w', ' ')
    mpg_text = remove_redundant_whitespace(mpg_text)
    mpg_city, mpg_hwy = MPG_REGEX.match(mpg_text).groups()
    mpg = Mileage(int(mpg_city), int(mpg_hwy))

    return KBBListing(miles=miles,
                      engine_description=scrape_icon_field(html, 'ENGINE_DESCRIPTION'),
                      mpg=mpg)


def scrape_icon_field(html, aria_label):
    miles_icon = assert_unique(html.find_all('div', attrs={'aria-label': aria_label}))
    for sib in miles_icon.parent.next_siblings:
        if sib.name == 'div' and sib.attrs == {'class': ['col-xs-10', 'margin-bottom-0']}:
            return sib.string or next(sib.stripped_strings)
    raise AssertionError(f"Icon field siblings don't match: {list(miles_icon.parent.next_siblings)}")


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
