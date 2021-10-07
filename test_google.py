import selenide as browser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

browser.driver = webdriver.Chrome(ChromeDriverManager().install())
browser.timeout = 2

query = browser.element('[name=q]')


browser.visit('https://google.com')
query.should_be_blank()
query.set_value('yashaka selene').press_enter()

browser.element('#rso .g').element('a').click()

browser.driver.quit()
