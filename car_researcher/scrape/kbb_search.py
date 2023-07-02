import json
import re
from dataclasses import dataclass
from typing import Optional

import bs4
from selenium.webdriver.common.by import By

from car_researcher.scrape.fetch import Fetcher, RequestsHtmlFetcher
from car_researcher.scrape.kbb_listing import MPG_REGEX
from car_researcher.scrape.scrape_utils import parse_int

VEHICLE_DETAILS_REGEX = re.compile('listingId=([0-9]+)')


class PriceRibbon:
    NONE = 'NONE'
    GREAT = 'GREAT'
    GOOD = 'GOOD'


@dataclass
class ListItem:
    vin: str
    title: str
    listing_url: str
    image_url: str
    price_usd: int
    production_year: int
    brand_name: str
    model_name: str
    miles: Optional[int]
    city_mpg: Optional[int]
    hwy_mpg: Optional[int]
    wheel_drive: str
    color: str
    seller_name: str
    seller_phone: str
    seller_address: str
    price_ribbon: str

    def json(self) -> str:
        return json.dumps(self.__dict__)


def scrape_kbb_search(url: str, fetcher: Fetcher):
    html = fetcher.proxy_get(url, (By.XPATH, '//h2[contains(text(), "Expert Reviews")]'))

    # items = html.find_all('div', attrs={'data-cmp': 'inventoryListing'})
    items = html.findChildren('script', attrs={'data-cmp': 'lstgSchema', 'type': 'application/ld+json'})
    return list(filter(lambda x: x is not None, [scrape_list_item(item) for item in items]))


def scrape_list_item(item: bs4.Tag):
    data = json.loads(item.string)
    if data['@type'] != ['Product', 'Car']:
        return None

    offers = data['offers']
    seller = offers['seller']

    vin = data['vehicleIdentificationNumber']
    title = data['name']
    listing_url = data['url']
    image_url = data['image']
    if offers['priceCurrency'] != 'USD' or 'InStock' not in offers['availability']:
        return None
    price = offers['price']
    production_year = data['productionDate']
    brand_name = data['brand']['name']['name'] if isinstance(data['brand']['name'], dict) else data['brand']['name']
    model_name = data['model'] if isinstance(data['model'], str) else data['model']['name']
    miles = parse_int(data['mileageFromOdometer']['value']) if data['mileageFromOdometer']['value'] else None
    if isinstance(data['fuelType'], dict) and data['fuelType']['group'] == 'Gas' and data['fuelEfficiency']:
        mileage_city, mileage_hwy = MPG_REGEX.match(data['fuelEfficiency']).groups()
        mileage_city, mileage_hwy = int(mileage_city), int(mileage_hwy)
    else:
        mileage_city, mileage_hwy = None, None
    drive = data['driveWheelConfiguration']
    color = data['color']
    seller_name = seller['name']
    seller_phone = seller['telephone']
    address = seller['address']
    seller_address = f"{address['streetAddress']}\n{address['addressLocality']}, {address['addressRegion']} {address['postalCode']}"
    price_ribbon = PriceRibbon.NONE
    if item.findChildren(string='GREAT PRICE'):
        price_ribbon = PriceRibbon.GREAT
    elif item.findChild(string='GOOD PRICE'):
        price_ribbon = PriceRibbon.GOOD

    return ListItem(vin, title, listing_url, image_url, price, production_year, brand_name, model_name, miles,
                    mileage_city, mileage_hwy, drive, color, seller_name, seller_phone, seller_address, price_ribbon)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        prog='scrape_kbb_search',
        description='Scrapes the search results from a KBB search url',
        epilog='Use --help for more info')
    parser.add_argument('url', help="The KBB search url to scrape")

    args = parser.parse_args()
    results = scrape_kbb_search(args.url, RequestsHtmlFetcher())
    print([r.json() for r in results])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
