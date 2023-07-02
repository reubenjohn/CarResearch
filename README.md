# CarResearch

Automates some of the car researching process in the US market through web scraping

## Setup

This is a [poetry](https://python-poetry.org/docs/basic-usage/) project, so make sure you have poetry version 1.2+
installed. Once installed, run the following command to set up the project and install dependencies.

    poetry install

## Usage

To scrape the data from a KBB search results screen:

    poetry run -- scrape-search "https://www.kbb.com/cars-for-sale/all/?isNewSearch=true&marketExtension=include&numRecords=25&searchRadius=0&showAccelerateBanner=false&sortBy=relevance&startYear=2023"

To scrape the data from the listing of a vehicle on KBB:

    poetry run -- scrape-listing "https://www.kbb.com/cars-for-sale/vehicledetails.xhtml?listingId=683600269"
