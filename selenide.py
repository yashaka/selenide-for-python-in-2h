#    selenide-for-python-in-2h
#    Copyright 2021 Iakiv Kramarenko
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#
#    This product includes software developed by Iakiv Kramarenko (yashaka@gmail.com)
#
#    This product bundles and modifies the wait.py from selenium project licensed by:
#    Copyright 2011-2021 Software Freedom Conservancy
#    Copyright 2004-2011 Selenium committers

from __future__ import annotations

from typing import Callable

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from wait import WebDriverWait

driver: WebDriver = ...
timeout: int = 4


def wait():
    return WebDriverWait(
        driver,
        timeout=timeout,
        ignored_exceptions=(WebDriverException,)
    )


# todo: remove redundant driver,
#       by using higher-order callable object
#       refactor to something like:
# class element_value_is_empty(object):
#
#     def __call__(self, element):
#         return element.locate().get_attribute('value') == ''
#
#     def __str__(self):
#         return f'value is empty'
class element_value_is_empty(object):
    def __init__(self, locate: Callable[[], WebElement]):
        self.locate = locate

    def __call__(self, driver):
        return self.locate().get_attribute('value') == ''

    def __str__(self):
        return f'value of element {self.locate} is empty'


class Element:
    def __init__(self, locate: Callable[[], WebElement]):
        self.locate = locate

    def should_be_blank(self) -> Element:
        # todo: consider passing self instead of self.locate ;)
        wait().until(element_value_is_empty(self.locate))
        return self

    def set_value(self, text) -> Element:
        # todo: log here and on all other commands the context of failure
        #       where the context is:
        #       1 what we wanted to call (command description)
        #       2 for which element? (locate description)
        #       this might be done in two steps:
        #       1 catching all errors inside command
        #         and raising new error with everything logged
        #       2 DRYing commands from duplication by higher-order function
        #         (the callable object might be redundant at this stage)
        #       3 finally, when added logging even passed commands,
        #         refactor higher-order fn to callable objct with str
        def command(driver):
            webelement = self.locate()
            webelement.clear()
            webelement.send_keys(text)

            return True

        wait().until(command)
        return self

    def press_enter(self) -> Element:
        def command(driver):
            webelement = self.locate()
            webelement.send_keys(Keys.ENTER)
            return True

        wait().until(command)
        return self

    def click(self):
        def command(driver):
            webelement = self.locate()
            webelement.click()
            return True

        wait().until(command)
        return self

    def element(self, selector: str) -> Element:
        def locate():
            original = self.locate()
            try:
                webelement = original.find_element(By.CSS_SELECTOR, selector)
                return webelement
            except Exception as error:
                # TODO: optimize: render outerHTML only on last try when wait
                outer_html = original.get_attribute('outerHTML')
                # todo: cut outer html by symbols limit
                # todo: move symbols limit to configuration
                # todo: log primarily the locator description not just outerHTML
                #       first: refactor from locate function
                #              to callable object with str
                #       finally: consider DRYing all element builders' callables
                #                with one class
                #                accepting on object init
                #                the locate-function and str-description ;)
                raise WebDriverException(
                    msg=f'failed to find inside {outer_html} '
                        f'the element by: {selector}'
                )

        return Element(locate)


def visit(url):
    driver.get(url)


def element(selector: str):
    return Element(lambda: driver.find_element(By.CSS_SELECTOR, selector))

# todo: finally: break down into modules by context
