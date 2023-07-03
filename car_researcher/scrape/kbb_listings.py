import logging
import os
from queue import Queue
from threading import Thread
from typing import List, Iterable

from car_researcher.scrape.fetch import Fetcher, RequestsHtmlFetcher
from car_researcher.scrape.kbb_listing import scrape_kbb_listing, KBBListing
from scrape.kbb_search import VEHICLE_DETAILS_REGEX


def scrape_kbb_listings(urls: List[str], fetcher: Fetcher, n_workers: int = 4) -> Iterable[KBBListing]:
    q = Queue()
    out = Queue()
    for url in urls:
        q.put(url, block=True)

    def worker():
        while not q.empty():
            url = q.get(block=True, timeout=1)
            try:
                listing = scrape_kbb_listing(url, fetcher, use_proxy=True)
                out.put(listing, block=True)
            except Exception as e:
                logging.error(f"Failed to scrape url '{url}'")
                print(e)

    threads = [Thread(target=worker) for _ in range(n_workers)]
    for thread in threads:
        thread.start()

    while any([t.is_alive() for t in threads]):
        while not out.empty():
            yield out.get(block=True, timeout=1)

    for thread in threads:
        thread.join()


def main():
    import argparse
    parser = argparse.ArgumentParser(
        prog='scrape_kbb_listings',
        description='Scrapes the key information from a batch of KBB listings',
        epilog='Use --help for more info')
    parser.add_argument('urls', help="File containing a KBB listing URL on each line")
    parser.add_argument('output', help="Destination directory in which to place the scraped data")

    args = parser.parse_args()
    with open(args.urls) as urls_file:
        urls = [url.strip() for url in urls_file.readlines()]

    os.makedirs(args.output, exist_ok=True)
    for listing in scrape_kbb_listings(urls, RequestsHtmlFetcher(), n_workers=1):
        listing_id = VEHICLE_DETAILS_REGEX.search(listing.url)[1]
        with open(f'{args.output}/{listing_id}.json', 'w') as listing_file:
            listing_file.write(listing.json())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
