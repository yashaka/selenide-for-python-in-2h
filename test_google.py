from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as condition
from webdriver_manager.chrome import ChromeDriverManager
import selenide as browser


browser.driver = webdriver.Chrome(ChromeDriverManager().install())
browser.timeout = 3


query = browser.Element('[name=q]')
result = By.CSS_SELECTOR, '#rso .g'
result_link = By.CSS_SELECTOR, 'a'

browser.visit('https://google.com')

query.should_be_blank()

# TODO: refactor below...

browser.driver.find_element(*query.locator).clear()
browser.driver.find_element(
    *query.locator
).send_keys('yashaka selene' + Keys.ENTER)

browser.driver.find_element(*result).find_element(*result_link).click()
browser.wait().until(condition.url_contains('github.com/yashaka/selene'))

browser.driver.quit()
