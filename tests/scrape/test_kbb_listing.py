import logging
from unittest import TestCase

import pytest

from car_researcher.scrape.kbb_listing import scrape_kbb_listing
from car_researcher.scrape.kbb_listing import KBBListing
from tests.scrape.fetch import StatelessTestVectorFetcher


class Test(TestCase):
    @pytest.fixture(autouse=True)
    def inject_fixtures(self, caplog):
        caplog.set_level(logging.INFO)

    def test_scrape_kbb_listing(self):
        listing = scrape_kbb_listing('kbb_listing', StatelessTestVectorFetcher())
        self.assertEqual(listing, KBBListing(43_293))
