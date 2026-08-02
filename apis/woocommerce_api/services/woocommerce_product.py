from apis.woocommerce_api.config.woocommerce_api_config import (
    WoocommerceApiConfig,
)
from apis.woocommerce_api.core.base_woocommerce_api import (
    BaseWoocommerceApi,
)
from apis.woocommerce_api.models.woocommerce_product_model import WoocommerceProductModel

from toolboxs.dict_utils import remove_none

# --
# ...
# --


class WoocommerceProduct(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:
        self.base_url = self.instance.config_dictionary.get("base_url")
        self.wp_media_url = self.instance.config_dictionary.get("wp_media_url")

        self.consumer_key = self.instance.config_dictionary.get("consumer_key")
        self.consumer_secret = self.instance.config_dictionary.get("consumer_secret")

        self.wp_user = self.instance.config_dictionary.get("wp_user")
        self.wp_password = self.instance.config_dictionary.get("wp_password")

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

    def __call__(self) -> str:
        pass

    # --
    # ...
    # --

    def get_product_by_name(self, name: str, record_per_page: int = 100):

        try:
            response = self.request(
                method="get",
                url=f"{self.base_url}{self.products_url}",
                auth=(self.consumer_key, self.consumer_secret),
                params={"per_page": record_per_page, "search": name},
            )

            self.prompt_on_screen(f"product modele: {response}")

            return response

        except Exception as exp:
            print(f"get_product_by_name: {exp}")

    # --
    # ...
    # --

    def get_all_products(self, record_per_page: int = 100):

        try:
            response = self.request(
                method="get",
                url=f"{self.base_url}{self.products_url}",
                auth=(self.consumer_key, self.consumer_secret),
                params={"per_page": record_per_page},
            )

            self.prompt_on_screen(f"products: {response}")

            return response

        except Exception as exp:
            print(f"get_products: {exp}")

    # --
    # ...
    # --

    def upload_product(self, product_model: WoocommerceProductModel):

        try:
            response = self.request(
                method="post",
                url=f"{self.base_url}{self.products_url}",
                auth=(self.consumer_key, self.consumer_secret),
                json=product_model.to_dict(),
            )

            self.prompt_on_screen(f"products: {response}")

            return response

        except Exception as exp:
            print(f"upload_product: {exp}")

    # --
    # ...
    # --

    def delete_product_by_product_id(self, product_id: int):

        try:
            response = self.request(
                method="delete",
                url=f"{self.base_url}{self.products_url}/{product_id}",
                auth=(self.consumer_key, self.consumer_secret),
                params={"force": True},
            )

            self.prompt_on_screen(f"product deleted: {response}")

            return response

        except Exception as exp:
            print(f"delete_product_by_product_id: {exp}")
