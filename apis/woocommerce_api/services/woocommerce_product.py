from apis.woocommerce_api.config.woocommerce_api_config import (
    WoocommerceApiConfig,
)
from apis.woocommerce_api.core.base_woocommerce_api import (
    BaseWoocommerceApi,
)
from apis.woocommerce_api.models.woocommerce_product_model import (
    WoocommerceProductModel,
)
from apis.woocommerce_api.models.search_in_woocommerce_model import SearchInWoocommerceModel

# --
# ...
# --


class WoocommerceProduct(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.base_url = self.config_dictionary.get("base_url")
        self.wp_media_url = self.config_dictionary.get("wp_media_url")

        self.consumer_key = self.config_dictionary.get("consumer_key")
        self.consumer_secret = self.config_dictionary.get("consumer_secret")

        self.wp_user = self.config_dictionary.get("wp_user")
        self.wp_password = self.config_dictionary.get("wp_password")

        self.products_url = self.config_dictionary.get("products_url")

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return WoocommerceApiConfig().get_dictionary()

    # --
    # ...
    # --

    def __call__(self) -> str:
        pass

    # --
    # ...
    # --

    def get_product_by_name(self, name: str, record_per_page: int = 100) -> WoocommerceProductModel:

        try:
            response = self.request(
                method="get",
                url=f"{self.base_url}{self.products_url}",
                auth=(self.consumer_key, self.consumer_secret),
                params={
                    "per_page": record_per_page,
                    "search": name,
                    "search_fields": "name",
                },
            )

            if not response:
                return None

            return WoocommerceProductModel(**response[0])

        except Exception as exp:
            self.prompt_on_screen(f"get_product_by_name: {exp}")

    # --
    # ...
    # --

    def get_all_products(self, record_per_page: int = 100) -> [WoocommerceProductModel]:

        try:
            response = self.request(
                method="get",
                url=f"{self.base_url}{self.products_url}",
                auth=(self.consumer_key, self.consumer_secret),
                params={"per_page": record_per_page},
            )
            woocommerce_product_models: list[WoocommerceProductModel] = []

            for product in response:
                woocommerce_product_models.append(WoocommerceProductModel(**product))

            return woocommerce_product_models

        except Exception as exp:
            self.prompt_on_screen(f"get_all_products: {exp}")

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
            self.prompt_on_screen(f"upload_product: {exp}")

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
            self.prompt_on_screen(f"delete_product_by_product_id: {exp}")

    # --
    # ...
    # --

    def get_product_by_search_in_woocommerce_model(self, search_in_woocommerce_model: SearchInWoocommerceModel) -> WoocommerceProductModel:

        try:
            response = self.request(
                method="get",
                url=f"{self.base_url}{self.products_url}",
                auth=(self.consumer_key, self.consumer_secret),
                params=search_in_woocommerce_model.filter,
            )

            if not response:
                return None

            elif isinstance(response, list):
                woocommerce_product_model = []
                for res in response:
                    woocommerce_product_model.append(WoocommerceProductModel(**res))
                return woocommerce_product_model

            else:
                return WoocommerceProductModel(**response)

        except Exception as exp:
            self.prompt_on_screen(f"get_product_by_search_in_woocommerce_model: {exp}")
