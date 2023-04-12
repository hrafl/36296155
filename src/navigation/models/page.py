from abc import ABC
from selenium.webdriver.remote.webdriver import WebDriver

class Page(ABC):
    
    def __init__(self, browser: WebDriver):
        self.browser = browser