from typing import Tuple

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as condition

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(ChromeDriverManager().install())
wait = WebDriverWait(
    driver,
    timeout=2,
    ignored_exceptions=(WebDriverException,)
)


class element_value_is_empty(object):
    def __init__(self, locator: Tuple[str, str]):
        self.locator = locator

    def __call__(self, driver: WebDriver):
        return driver.find_element(*self.locator).get_attribute('value') == ''

    def __str__(self):
        return f'value of element {self.locator} is empty'


query = By.CSS_SELECTOR, '[name=q]'
result = By.CSS_SELECTOR, '#rso .g'
result_link = By.CSS_SELECTOR, 'a'

driver.get('https://google.com')

wait.until(element_value_is_empty(query))

# driver.find_element(*query).clear()
driver.find_element(*query).send_keys('yashaka selene' + Keys.ENTER)

driver.find_element(*result).find_element(*result_link).click()
wait.until(condition.url_contains('github.com/yashaka/selene'))

driver.quit()
