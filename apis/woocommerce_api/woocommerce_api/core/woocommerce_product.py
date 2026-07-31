from apis.woocommerce_api.woocommerce_api.core.base_woocommerce_api import BaseWoocommerceApi
from apis.woocommerce_api.woocommerce_api.config.woocommerce_api_config import (
    WoocommerceApiConfig,
)
from apis.models.woocommerce_category_model import WoocommerceCategoryModel
import CONSTS
from  apis.models.woocommerce_product_model import WoocommerceProductModel
import json

# --
# ...
# --


class WoocommerceProduct(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:
        self.base_url = self.instance.config_dictionary.get("base_url")
        self.wp_media_url = self.instance.config_dictionary.get("wp_media_url")

        self.consumer_key= self.instance.config_dictionary.get("consumer_key")
        self.consumer_secret= self.instance.config_dictionary.get("consumer_secret")

        self.wp_user= self.instance.config_dictionary.get("wp_user")
        self.wp_password= self.instance.config_dictionary.get("wp_password")

        self.products_url = self.instance.config_dictionary.get("products_url")

        self.prompt_on_screen(f"{__class__.__name__}, {id(__class__)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return WoocommerceApiConfig().instance.dictionary

    # --
    # ...
    # --

    def __call__(self, category_id) -> str:
        self.get_products()

    # --
    # ...
    # --

    def get_all_products(self, record_per_page:int = 100):

        try:

            response = self.request(
                method="get",
                url=f"{self.base_url}{self.products_url}",
                auth=(self.consumer_key, self.consumer_secret),
                params = {
                    "per_page": record_per_page
                    }
            )

            self.prompt_on_screen(
                f"products: {response}"
            )

            return response
        
        except Exception as exp:
            print(f"get_products: {exp}")

    # --
    # ...
    # --

    def upload_products(self, products_model:list[WoocommerceProductModel]):

        try:

            for product_model in products_model:

                response = self.request(
                    method="post",
                    url=f"{self.base_url}{self.products_url}",
                    auth=(self.consumer_key, self.consumer_secret),
                    json = product_model.to_dict()
                )

                self.prompt_on_screen(
                    f"products: {response}"
                )

            return
        
        except Exception as exp:
            print(f"upload_products: {exp}")



def test():
    WoocommerceProduct().get_all_products()
    category_model = WoocommerceCategoryModel(id=26)
    product_model = WoocommerceProductModel(name='hahaha', categories=[category_model])

    WoocommerceProduct().upload_products([product_model])