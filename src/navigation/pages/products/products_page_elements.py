from src.navigation.models.page_element import PageElement
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By

class Paginator(PageElement):

    def map_element(self):
        self.element = self.page.browser.find_element(By.ID, "itemsPager")

    def _get_next_page_button(self) -> WebElement:
        try:
            element = self.element.find_element(By.CLASS_NAME, "next").find_element(By.TAG_NAME, "a")
            return element
        except:
            return None

    def is_there_next_page(self) -> bool:
        next_page_element = self._get_next_page_button()
        if next_page_element is None:
            return False
        else:
            return True

    def go_to_next_page(self):

        next_page_element = self._get_next_page_button()

        if not next_page_element is None:
            next_page_element.click()


class ProductCard(PageElement):

    def map_element(self):
        pass

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


class ProductCardList(PageElement):
    
    def map_element(self):
        self.element = self.page.browser.find_element(By.ID, "productList")

        # map children
        product_cards_form = self.element.find_elements(By.TAG_NAME, "form")

        for form in product_cards_form:
            product_card = form.find_element(By.CLASS_NAME, "row")
            self.children.append(ProductCard(self.page, product_card))