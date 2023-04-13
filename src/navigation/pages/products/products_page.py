
from typing import List
from src.navigation.models.page import Page
from src.navigation.pages.products.products_page_elements import Paginator, ProductCard, ProductCardList
from selenium.webdriver.common.by import By

class ProductsPage(Page):

    @property
    def paginator(self):
        element = Paginator(self)
        element.load_element()
        return element

    @property
    def product_card_list(self) -> List[ProductCard]:
        element = ProductCardList(self)
        element.load_element()
        return element.children
    
    def hide_dialogs(self):

        elements = self.browser.find_elements(By.XPATH, "//*[contains(@class, 'dialog')]")

        for element in elements:
            self._hide_element(element)

        elements = self.browser.find_elements(By.CSS_SELECTOR, 'div[role="dialog"]')

        for element in elements:
            self._hide_element(element)

    def _hide_element(self, element):
        self.browser.execute_script("arguments[0].style.display = 'none';", element)

    def reduce_zoom_level(self, zoom_level: float):
        self.browser.execute_script("document.body.style.zoom = '{}'".format(zoom_level))
