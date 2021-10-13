from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


driver = webdriver.Chrome(ChromeDriverManager().install())
wait = WebDriverWait(
    driver,
    timeout=2,
    ignored_exceptions=(WebDriverException,)
)


class element_value_is_empty(object):
    def __init__(self, selector: str):
        self.selector = selector

    def __call__(self, driver: WebDriver):
        return driver.find_element(
            By.CSS_SELECTOR, self.selector
        ).get_attribute('value') == ''

    def __str__(self):
        return f'value of element {self.selector} is empty'


query = By.CSS_SELECTOR, '[name=q]'
result = By.CSS_SELECTOR, '#rso .g'
result_link = By.CSS_SELECTOR, 'a'

driver.get('https://google.com')

wait.until(element_value_is_empty('[name=q]'))

# driver.find_element(*query).clear()
driver.find_element(*query).send_keys('yashaka selene' + Keys.ENTER)

driver.find_element(*result).find_element(*result_link).click()
# todo: assert on github.com/yashaka/selene page

driver.quit()
