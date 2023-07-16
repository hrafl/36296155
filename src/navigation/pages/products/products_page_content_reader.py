from typing import List
from pydantic import BaseModel
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

from src.models.product import Product
from src.services import browser_service


class ProductCard(object):

    def __init__(self, element: WebElement) -> None:
        self.element = element

    def _get_descriptions_container(self) -> WebElement:
        element = self.element.find_elements(By.CSS_SELECTOR, "div.row > div")[1]
        return element
    
    def _get_attributes_container(self) -> WebElement:
        element = self.element.find_elements(By.CSS_SELECTOR, "div.row > div")[2]
        return element
    
    def _get_product_details_and_actions_container(self) -> WebElement:
        element = self.element.find_elements(By.CSS_SELECTOR, "div.row > div")[3].find_element(By.CSS_SELECTOR, "div > div")
        return element

    def get_description_1(self) -> str:
        try:
            descriptions_container = self._get_descriptions_container()
            text = descriptions_container.find_element(By.CLASS_NAME, "title").find_element(By.TAG_NAME, "a").text.strip()
            return text
        except: pass

    def get_description_2(self) -> str:
        try:
            descriptions_container = self._get_descriptions_container()
            text = descriptions_container.find_element(By.CLASS_NAME, "description").text.split('\n')[0]
            return text
        except: pass

    def get_description_3(self) -> str:
        try:
            descriptions_container = self._get_descriptions_container()
            text = descriptions_container.find_element(By.CLASS_NAME, "description").text.split('\n')[1]
            return text
        except: pass

    def get_article_number(self) -> str:
        try:
            descriptions_container = self._get_descriptions_container()
            text = descriptions_container.find_element(By.CLASS_NAME, "artnum").text.strip()
            return text
        except: pass

    def get_dimension(self) -> str:
        try:
            attributes_container = self._get_attributes_container()
            text = attributes_container.find_element(By.CLASS_NAME, "attributes").find_elements(By.TAG_NAME, "li")[0].find_element(By.TAG_NAME, "span").text.strip()
            return text
        except: pass

    def get_diameter(self) -> str:
        try:
            attributes_container = self._get_attributes_container()
            text = attributes_container.find_element(By.CLASS_NAME, "attributes").find_elements(By.TAG_NAME, "li")[1].find_element(By.TAG_NAME, "span").text.strip()
            return text
        except: pass

    def get_wgr(self) -> int:
        try:
            attributes_container = self._get_attributes_container()
            text = attributes_container.find_element(By.CLASS_NAME, "additional_attributes").find_element(By.TAG_NAME, "span").text.strip()
            return int(text)
        except: pass

    def get_unit_of_measure(self) -> str:
        try:
            product_details_and_actions_container = self._get_product_details_and_actions_container()
            text = product_details_and_actions_container.text.strip().split('\n')[0]
            return text
        except: pass
    
    def get_price(self) -> str:
        try:
            product_details_and_actions_container = self._get_product_details_and_actions_container()
            span_list = product_details_and_actions_container.find_elements(By.TAG_NAME, "span")
            for span in span_list:
                if "productPrice_productList" in span.get_attribute("id"):
                    return span.text.strip()
        except: pass

    def get_weight(self) -> str:
        try:
            product_details_and_actions_container = self._get_product_details_and_actions_container()
            span_list = product_details_and_actions_container.find_elements(By.TAG_NAME, "span")
            for span in span_list:
                if "productPricePerUnit_productList" in span.get_attribute("id"):
                    return span.text.strip()
        except: pass

    def to_product(self) -> Product:

        product = Product()
        product.description_1 = self.get_description_1()
        product.description_2 = self.get_description_2()
        product.description_3 = self.get_description_3()
        product.article_number = self.get_article_number()
        product.dimension = self.get_dimension()
        product.diameter = self.get_diameter()
        product.wgr = self.get_wgr()
        product.unit_of_measure = self.get_unit_of_measure()
        product.price = self.get_price()
        product.weight = self.get_weight()

        return product

class ProductsPageContentReader(object):

    def __init__(self, browser: WebDriver) -> None:
        self.browser = browser

    def is_there_next_page(self) -> bool:
        paginator_element: WebElement = None
        self.browser.implicitly_wait(5)
        try:
            paginator_element = self.browser.find_element(By.ID, "itemsPager")
        except: pass

        self.browser.implicitly_wait(browser_service.WAIT_LIMIT)

        if paginator_element is None:
            return False
        
        next_page_button = None
        try:
            next_page_button = paginator_element.find_element(By.CLASS_NAME, "next").find_element(By.TAG_NAME, "a")
        except: pass

        if next_page_button is None:
            return False
        else:
            return True

    def get_products(self) -> List[Product]:

        products = []

        product_cards_container = self.browser.find_element(By.ID, "productList")
        if product_cards_container is None:
            return None
        
        product_cards_form = product_cards_container.find_elements(By.TAG_NAME, "form")
        if product_cards_form is None:
            return None
        
        for form in product_cards_form:
            product_card = form.find_element(By.CLASS_NAME, "row")
            product_card = ProductCard(product_card)
            products.append(product_card.to_product())

        return products