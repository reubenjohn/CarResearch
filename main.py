from typing import TypeVar

from bs4 import BeautifulSoup, ResultSet, Tag
from requests_html import HTMLSession
import re

LISTING_CERTIFIED_2020_FORT_ESCAPE = 'https://www.kbb.com/cars-for-sale/vehicledetails.xhtml?listingId=683600269'
KBB_LISTING_MILES_REGEX = re.compile('([0-9,]+) miles')


def main():
    session = HTMLSession()
    r = scrape_kbb_listing(LISTING_CERTIFIED_2020_FORT_ESCAPE)


E = TypeVar("E")


def assert_unique(l: ResultSet) -> Tag:
    assert len(l) == 1, "Expected a unique result, but found: " + str(l)
    return l[0]


def scrape_kbb_listing(url: str):
    r = HTMLSession().get(url)
    html = BeautifulSoup(r.html.html, features='html.parser')
    miles_icon = assert_unique(html.find_all('div', attrs={'aria-label': 'MILEAGE'}))
    miles = KBB_LISTING_MILES_REGEX.match(miles_icon.parent.next_sibling.string)[1]
    print(miles)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
