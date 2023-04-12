
from typing import List
from src.navigation.models.page import Page
from src.navigation.pages.products.products_page_elements import Paginator, ProductCard, ProductCardList


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