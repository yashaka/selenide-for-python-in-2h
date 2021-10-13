from typing import Tuple

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

driver: WebDriver = ...
timeout: int = 4


def wait():
    return WebDriverWait(
        driver,
        timeout=timeout,
        ignored_exceptions=(WebDriverException,)
    )


def visit(url):
    driver.get(url)


class element_value_is_empty(object):
    def __init__(self, locator: Tuple[str, str]):
        self.locator = locator

    def __call__(self, driver: WebDriver):
        return driver.find_element(*self.locator).get_attribute('value') == ''

    def __str__(self):
        return f'value of element {self.locator} is empty'


class Element:
    def __init__(self, selector: str):
        self.locator = By.CSS_SELECTOR, selector

    def should_be_blank(self):
        wait().until(element_value_is_empty(self.locator))
