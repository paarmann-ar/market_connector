import html

from apis.woocommerce_api.config.woocommerce_api_config import (
    WoocommerceApiConfig,
)
from apis.woocommerce_api.core.base_woocommerce_api import (
    BaseWoocommerceApi,
)
from apis.woocommerce_api.models.woocommerce_category_model import (
    WoocommerceCategoryModel,
)

# --
# ...
# --


class WoocommerceCategory(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.base_url = self.config_dictionary.get("base_url")
        self.wp_media_url = self.config_dictionary.get("wp_media_url")

        self.consumer_key = self.config_dictionary.get("consumer_key")
        self.consumer_secret = self.config_dictionary.get("consumer_secret")

        self.wp_user = self.config_dictionary.get("wp_user")
        self.wp_password = self.config_dictionary.get("wp_password")

        self.category_url = self.config_dictionary.get("category_url")

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
        pass

    # --
    # ...
    # --

    def get_category_by_name(self, name: str, record_per_page: int = 100):

        response = self.request(
            method="get",
            url=f"{self.base_url}{self.category_url}",
            auth=(self.consumer_key, self.consumer_secret),
            params={
                "per_page": record_per_page,
            },
        )

        if not response:
            return None

        for category in response:
            if html.unescape(category["name"].lower()) == name.lower():
                return WoocommerceCategoryModel.from_api(category)

    # --
    # ...
    # --

    def get_all_categories(self, record_per_page: int = 100):

        try:
            response = self.request(
                method="get",
                url=f"{self.base_url}{self.category_url}",
                auth=(self.consumer_key, self.consumer_secret),
                params={"per_page": record_per_page},
            )

            self.prompt_on_screen(f"categories: {response}")

        except Exception as exp:
            self.prompt_on_screen(f"get_all_categories: {exp}")

    # --
    # ...
    # --

    def upload_category(self, category_model: WoocommerceCategoryModel):

        try:
            response = self.request(
                method="post",
                url=f"{self.base_url}{self.category_url}",
                auth=(self.consumer_key, self.consumer_secret),
                json=category_model.to_dict(),
            )

            self.prompt_on_screen(f"categoriey to upload: {response}")

            woocommerce_category_model = WoocommerceCategoryModel.from_api(response)
            return woocommerce_category_model

        except Exception as exp:
            self.prompt_on_screen(f"upload_category: {exp}")

    # --
    # ...
    # --

    def resolve_or_upload(self, woocommerce_category_model: WoocommerceCategoryModel) -> WoocommerceCategoryModel:

        category = self.get_category_by_name(woocommerce_category_model.name)

        if category:
            return category

        return self.upload_category(WoocommerceCategoryModel(name=woocommerce_category_model.name))

    # --
    # ...
    # --

    def delete_category_by_category_id(self, category_id: int):

        try:
            response = self.request(
                method="delete",
                url=f"{self.base_url}{self.category_url}/{category_id}",
                auth=(self.consumer_key, self.consumer_secret),
                params={"force": True},
            )

            self.prompt_on_screen(f"category deleted: {response}")

            return response

        except Exception as exp:
            self.prompt_on_screen(f"delete_category_by_category_id: {exp}")
