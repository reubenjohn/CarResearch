import logging
import os.path
from typing import Tuple

from bs4 import BeautifulSoup

from car_researcher.scrape.fetch import Fetcher

VECTORS_PATH = 'tests/vectors/html'


class StatelessTestVectorFetcher(Fetcher):
    def __init__(self):
        self._rendered_response = None
        self._url = None

    def proxy_get(self, url: str, completion_locator: Tuple[str, str]) -> BeautifulSoup:
        if self._rendered_response:
            return self._rendered_response
        self._url = url
        html_path = os.path.realpath(f'{VECTORS_PATH}/{url}.html')
        logging.info(f"Reading test vector: {html_path}")
        with open(html_path) as html_file:
            return BeautifulSoup(''.join(html_file.readlines()), features='html.parser')

    def render(self):
        html_path = os.path.realpath(f'{VECTORS_PATH}/{self._url}.rendered.html')
        logging.info(f"Reading test vector: {html_path}")
        with open(html_path) as html_file:
            self._rendered_response = BeautifulSoup(''.join(html_file.readlines()))
