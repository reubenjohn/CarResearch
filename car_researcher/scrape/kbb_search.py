import re
from dataclasses import dataclass
from enum import Enum

import bs4
from selenium.webdriver.common.by import By

from car_researcher.scrape.fetch import Fetcher, RequestsHtmlFetcher
from car_researcher.scrape.scrape_utils import remove_redundant_whitespace, assert_unique, parse_int

VEHICLE_DETAILS_REGEX = re.compile('listingId=([0-9]+)')


class PriceRibbon(Enum):
    NONE = 0
    GREAT = 1
    GOOD = 2


@dataclass
class ListItem:
    title: str
    first_price: int
    listing_id: str
    price_ribbon: PriceRibbon
    image_url: str


def scrape_kbb_search(url: str, fetcher: Fetcher):
    html = fetcher.proxy_get(url, (By.XPATH, '//h2[contains(text(), "Expert Reviews")]'))

    items = html.find_all('div', attrs={'data-cmp': 'inventoryListing'})
    return [scrape_list_item(item) for item in items]


def scrape_list_item(item: bs4.Tag):
    title_tag = item.findChild('h3', attrs={'data-cmp': 'subheading'})
    title = remove_redundant_whitespace(title_tag.string)
    listing_id = re.compile(VEHICLE_DETAILS_REGEX).search(title_tag.findParent('a').attrs['href'])[1]

    price_ribbon = PriceRibbon.NONE
    if item.findChildren(string='GREAT PRICE'):
        price_ribbon = PriceRibbon.GREAT
    elif item.findChild(string='GOOD PRICE'):
        price_ribbon = PriceRibbon.GOOD

    first_price = parse_int(assert_unique(item.findChildren('span', 'first-price')).string)
    first_price = parse_int(assert_unique(item.findChildren('span', 'first-price')).string)

    return ListItem(title, first_price, listing_id, price_ribbon)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        prog='scrape_kbb_search',
        description='Scrapes the search results from a KBB search url',
        epilog='Use --help for more info')
    parser.add_argument('url', help="The KBB search url to scrape")

    args = parser.parse_args()
    listing = scrape_kbb_search(args.url, RequestsHtmlFetcher())
    print(listing)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
