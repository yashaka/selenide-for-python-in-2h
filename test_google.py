import selenide as browser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as condition

# todo: refactor to `browser = Browser(driver=..., timeout=..., )
# todo: refactor to `browser = Browser(Config(driver=..., timeout=..., )
browser.driver = webdriver.Chrome(ChromeDriverManager().install())
browser.timeout = 2
# todo: configure base_url
# todo: finally: configure logging all commands (e.g. to integrate with allure)

query = browser.element('[name=q]')
# todo: support XPath


browser.visit('https://google.com')
# todo: finally: query.should(match.blank)
query.should_be_blank()
query.set_value('yashaka selene').press_enter()
# todo: add more commands, like:
# (
#     query
#     .should_have_attribute('value', '')
#     .should_have_text('')
#     .clear()
#     .type('yashaka selene')
#     .double_click()
# )

# todo: refactor to: browser.all('#rso .g').first.element('a').click()
#       where all -> Elements (object of a collection class)
browser.element('#rso .g').element('a').click()  # todo: add more commands like:
# (
#     browser.all('#rso .g').by(match.text('github'))
#     .should(match.size(2))
#     [1]
#     .element('a').click()
# )


# todo: browser.should(match.url_containing('github.com/yashaka/selene'))g
browser.wait().until(condition.url_contains('github.com/yashaka/selene'))

# todo: consider refactoring to browser.quit()
browser.driver.quit()
