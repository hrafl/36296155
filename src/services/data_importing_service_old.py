import os

if __name__ == "__main__":
    import sys
    sys.path.append(os.path.abspath('.'))

import json
from typing import List
from src.models.product import Product
from src.models.products_data_provider import ProductsDataProvider
from src.navigation.pages.products.products_page import ProductsPage
from src.services import browser_service
from selenium.webdriver.remote.webdriver import WebDriver
import pandas as pd

reading_config: dict
browser: WebDriver
products_data_provider = ProductsDataProvider()

def go_to_products_page(topic: str, sub_topic: str):
    pass

def read_products(material_type: str, product_type: str, characteristic: str):

    global products_data_provider
    global browser

    url = f"https://shop.ibl-raimund.de/{material_type}/{product_type}/{characteristic}"
    browser.get(url)

    products_page = ProductsPage(browser)
    # products_page.reduce_zoom_level(0.8)


    while True:
        for product_card in products_page.product_card_list:
            product = Product()
            product.description_1 = product_card.get_description_1()
            product.description_2 = product_card.get_description_2()
            product.description_3 = product_card.get_description_3()
            product.article_number = product_card.get_article_number()
            product.dimension = product_card.get_dimension()
            product.diameter = product_card.get_diameter()
            product.wgr = product_card.get_wgr()
            product.unit_of_measure = product_card.get_unit_of_measure()
            product.price = product_card.get_price()
            product.weight = product_card.get_weight()
            product.material = material_type
            product.type = product_type
            product.characteristic = characteristic

            products_data_provider.products.append(product)

        if products_page.paginator.is_there_next_page():
            products_page.paginator.go_to_next_page()

        else:
            break

def config_dataframe_to_export(df: pd.DataFrame) -> pd.DataFrame:

    df = df.drop("material", axis=1)

    columns = {
        "topic_1": "Topic 1", 
        "topic_2": "Topic 2", 
        "description_1": "Description 1",
        "description_2": "Description 2",
        "description_3": "Description 3",
        "article_number": "Article No. Asr",
        "dimension": "Abmessung",
        "diameter": "Durchmesser",
        "wgr": "WGR",
        "unit_of_measure": "unit of measure",
        "price": "Price",
        "weight": "Weight"
    }
    df = df.rename(columns=columns)

    col_index = range(1, len(df) + 1)
    df.insert(0, "No.", col_index)
    
    return df

def export_result_to_excel():
    df = pd.DataFrame(products_data_provider.dict()["products"])
    df = config_dataframe_to_export(df)
    df.to_excel("products.xlsx", index=False)

def export_result_to_csv():
    dt = pd.DataFrame(products_data_provider.dict()["products"])
    df = config_dataframe_to_export(df)
    dt.to_csv("products.csv", index=False)

def export_resul_to_json():
    with open("products.json", "w", encoding="utf-8") as arquivo:
        json.dump(products_data_provider.dict()["products"], arquivo, ensure_ascii=False)

def export_result(file_type: str):

    if file_type == "json":
        export_resul_to_json()
    elif file_type == "csv":
        export_result_to_csv()
    elif file_type == "xlsx":
        export_result_to_excel()
    else:
        export_result_to_excel()

def execute():

    global browser
    global reading_config

    print("## Starting application...")
    
    browser = browser_service.create_new_instance()
 
    reading_config = json.load(open("reading.config.json"))
    
    os.system('cls')
    print("## Starting application... [OK]", end="\r")

    for material_type in reading_config["materialType"]:
        for product_type in material_type["productTypes"]:
            for characteristic in product_type["characteristics"]:
                print("")
                print(f'## Collecting data -> material type: {material_type["name"]} | product type: {product_type["name"]} | characteristic: {characteristic["name"]}', end="\r")
                read_products(material_type["name"], product_type["name"], characteristic["name"])
                print(f'## Collecting data -> material type: {material_type["name"]} | product type: {product_type["name"]} | characteristic: {characteristic["name"]} [OK]', end="\r")

    browser.quit()
    
    print("")
    print("## Starting to export data collected...", end="\r")
    export_result(str(reading_config["exportFileType"]).lower().strip())
    print("## Starting to export data collected... [OK]", end="\r")
    print("")
    print("-- Closing application...")