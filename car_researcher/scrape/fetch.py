from abc import ABC, abstractmethod

from bs4 import BeautifulSoup
from requests_html import HTMLSession


class Fetcher(ABC):
    @abstractmethod
    def get(self, url: str) -> BeautifulSoup:
        pass

    @abstractmethod
    def render(self):
        pass


class RequestsHtmlFetcher(Fetcher):
    def __init__(self):
        self._session = HTMLSession()
        self._response = None

    def get(self, url: str) -> BeautifulSoup:
        self._response = self._session.get(url)
        return BeautifulSoup(self._response.html.html, features='html.parser')

    def render(self):
        self._response.html.render()
