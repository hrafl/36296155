from abc import ABC, abstractmethod

from pydantic import BaseModel
from src.navigation.models.page import Page
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from typing import List
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from src.services.browser_service import WAIT_LIMIT

class PageElement(ABC):    
    
    def __init__(self, page: Page, element: WebElement = None):
        self.page = page
        self.element = element
        self.children: List[PageElement] = []

    #Properties
    @property
    def text(self):
        """ Get the text inside element """
        return self.element.text

    @property
    def is_enabled(self):
        """ Whether the element is enabled. """
        return self.element.is_enabled()

    @property
    def is_displayed(self):
        """ Whether the element is visible to a user. """
        return self.element.is_displayed()

    @property
    def is_selected(self):
        """ Returns whether the element is selected. Can be used to check if a checkbox or radio button is selected. """
        return self.element.is_selected()

    @property
    def value(self):
        """ Get and set input's value. """

        if self.element is None:
            return ''

        value = self.get_input_element().get_attribute("value")
        value = value.replace(u'\xa0', u' ')

        return value
        
    @value.setter
    def value(self, value):
        self.get_input_element().send_keys(value)

    # Navigation methods
    def click(self):
        self.element.click()

    def wait_until_become_visible(self, timeout = 20):
        wdw = WebDriverWait(driver = self.page.browser, timeout = timeout, poll_frequency= 0.2)
        wdw.until(EC.visibility_of(self.element))

    ## Other methods
    @abstractmethod
    def map_element(self):
        """ Method user to set 'element' property of current page element. Use 'self.page.browser.find_element()' method to map the element. """

    def load_element(self):

        start = datetime.now()

        while self.element is None:
            now = datetime.now()

            self.map_element()

            if self.element is not None or (now - start).total_seconds() > WAIT_LIMIT:
                break    

    def get_input_element(self) -> WebElement:

        if self.element is None:
            return None

        input_element: WebElement = None

        if self.element.tag_name.lower() == "input":
            input_element = self.element
        else:
            input_element = self.element.find_element(By.TAG_NAME, "input")

        return input_element