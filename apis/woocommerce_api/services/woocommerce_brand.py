import html

from apis.woocommerce_api.config.woocommerce_api_config import (
    WoocommerceApiConfig,
)
from apis.woocommerce_api.core.base_woocommerce_api import (
    BaseWoocommerceApi,
)
from apis.woocommerce_api.models.woocommerce_brand_model import WoocommerceBrandModel

# --
# ...
# --


class WoocommerceBrand(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.base_url = self.config_dictionary.get("base_url")
        self.wp_media_url = self.config_dictionary.get("wp_media_url")

        self.consumer_key = self.config_dictionary.get("consumer_key")
        self.consumer_secret = self.config_dictionary.get("consumer_secret")

        self.wp_user = self.config_dictionary.get("wp_user")
        self.wp_password = self.config_dictionary.get("wp_password")

        self.brand_url = self.config_dictionary.get("brand_url")

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

    def __call__(self, category_id) -> str:
        self.get_all_brands()

    # --
    # ...
    # --

    def get_brand_by_name(self, name: str, record_per_page: int = 100):

        response = self.request(
            method="get",
            url=f"{self.base_url}{self.brand_url}",
            auth=(self.consumer_key, self.consumer_secret),
            params={"per_page": record_per_page},
        )

        for brand in response:
            if html.unescape(brand["name"].lower()) == name.lower():
                return WoocommerceBrandModel.from_api(brand)

        return None

    # --
    # ...
    # --

    def get_all_brands(self, record_per_page: int = 100):

        try:
            brands: list = [dict]

            response = self.request(
                method="get",
                url=f"{self.base_url}{self.brand_url}",
                auth=(self.consumer_key, self.consumer_secret),
                params={"per_page": record_per_page},
            )

            for res in response:
                brands.append({"id": res["id"], "name": res["name"]})

            self.prompt_on_screen(f"brands: {brands}")

            return brands

        except Exception as exp:
            print(f"get_all_brands: {exp}")

    # --
    # ...
    # --

    def upload_brand(self, brand_model: WoocommerceBrandModel):

        try:
            response = self.request(
                method="post",
                url=f"{self.base_url}{self.brand_url}",
                auth=(self.consumer_key, self.consumer_secret),
                json=brand_model.to_dict(),
            )

            self.prompt_on_screen(f"brands: {response}")

            woocommerce_brand_model = WoocommerceBrandModel.from_api(response)
            return woocommerce_brand_model

        except Exception as exp:
            print(f"upload_brand: {exp}")

    # --
    # ...
    # --

    def resolve_or_upload(self, woocommerce_brand_model: WoocommerceBrandModel):

        brand = self.get_brand_by_name(woocommerce_brand_model.name)

        if brand:
            return brand

        return self.upload_brand(
            WoocommerceBrandModel(name=woocommerce_brand_model.name)
        )

    # --
    # ...
    # --

    def delete_brand_by_brand_id(self, brand_id: int):

        try:
            response = self.request(
                method="delete",
                url=f"{self.base_url}{self.brand_url}/{brand_id}",
                auth=(self.consumer_key, self.consumer_secret),
                params={"force": True},
            )

            self.prompt_on_screen(f"brand deleted: {response}")

            return response

        except Exception as exp:
            print(f"delete_brand_by_brand_id: {exp}")


def test():
    WoocommerceBrand().get_all_brands()
    WoocommerceBrand().resolve_or_upload("hahaha")
