from abc import ABC, abstractmethod
from time import sleep
from typing import Tuple

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class Fetcher(ABC):
    @abstractmethod
    def proxy_get(self, url: str, completion_locator: Tuple[str, str]) -> BeautifulSoup:
        pass

    @abstractmethod
    def render(self, **kwargs):
        pass


class RequestsHtmlFetcher(Fetcher):
    def __init__(self):
        self._response = None
        self._driver = webdriver.Edge()

    def proxy_get(self, url: str, completion_locator: Tuple[str, str], via_proxy=False) -> BeautifulSoup:
        self._driver.get(url)
        try:
            wait = WebDriverWait(self._driver, 10)

            if via_proxy:
                element_located = lambda *locator: wait.until(expected_conditions.presence_of_element_located(*locator))

                element_located((By.ID, 'url')).send_keys(url)
                element_located((By.ID, 'requestSubmit')).click()

            wait = WebDriverWait(self._driver, 1)
            element_located = lambda *locator: wait.until(expected_conditions.presence_of_element_located(*locator))
            for _ in range(10):
                try:
                    sleep(.1)  # To avoid referencing the html from the previous page below
                    element_located((By.TAG_NAME, 'html')).send_keys(Keys.END)
                    if element_located(completion_locator):
                        return BeautifulSoup(self._driver.page_source, features='html.parser')
                except TimeoutException:
                    pass
            raise RuntimeError("Completion condition could not be achieved")
        finally:
            self._driver.quit()

    def render(self, **kwargs):
        self._response.html.render(**kwargs)
