import html

from apis.woocommerce_api.config.woocommerce_api_config import (
    WoocommerceApiConfig,
)
from apis.woocommerce_api.core.base_woocommerce_api import (
    BaseWoocommerceApi,
)
from apis.woocommerce_api.models.woocommerce_tag_model import WoocommerceTagModel

# --
# ...
# --


class WoocommerceTag(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.base_url = self.config_dictionary.get("base_url")
        self.wp_media_url = self.config_dictionary.get("wp_media_url")

        self.consumer_key = self.config_dictionary.get("consumer_key")
        self.consumer_secret = self.config_dictionary.get("consumer_secret")

        self.wp_user = self.config_dictionary.get("wp_user")
        self.wp_password = self.config_dictionary.get("wp_password")

        self.tag_url = self.config_dictionary.get("tag_url")

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
        self.get_all_tags()

    # --
    # ...
    # --

    def get_tag_by_name(self, name: str, record_per_page: int = 100):

        response = self.request(
            method="get",
            url=f"{self.base_url}{self.tag_url}",
            auth=(self.consumer_key, self.consumer_secret),
            params={"per_page": record_per_page},
        )

        for tag in response:
            if html.unescape(tag["name"].lower()) == name.lower():
                return WoocommerceTagModel.from_api(tag)

        return None

    # --
    # ...
    # --

    def get_all_tags(self, record_per_page: int = 100) -> list[WoocommerceTagModel]:

        try:
            tags: list = [dict]

            response = self.request(
                method="get",
                url=f"{self.base_url}{self.tag_url}",
                auth=(self.consumer_key, self.consumer_secret),
                params={"per_page": record_per_page},
            )

            self.prompt_on_screen(f"tags: {response}")

            return tags

        except Exception as exp:
            self.prompt_on_screen(f"get_all_tags: {exp}")

    # --
    # ...
    # --

    def upload_tag(self, tag_model: WoocommerceTagModel):

        try:
            response = self.request(
                method="post",
                url=f"{self.base_url}{self.tag_url}",
                auth=(self.consumer_key, self.consumer_secret),
                json=tag_model.to_dict(),
            )

            self.prompt_on_screen(f"tags: {response}")

            woocommerce_tag_model = WoocommerceTagModel.from_api(response)
            return woocommerce_tag_model

        except Exception as exp:
            self.prompt_on_screen(f"upload_tag: {exp}")

    # --
    # ...
    # --

    def resolve_or_upload(self, woocommerce_tag_model: WoocommerceTagModel):

        tag = self.get_tag_by_name(woocommerce_tag_model.name)

        if tag:
            return tag

        return self.upload_tag(WoocommerceTagModel(name=woocommerce_tag_model.name))

    # --
    # ...
    # --

    def delete_tag_by_tag_id(self, tag_id: int):

        try:
            response = self.request(
                method="delete",
                url=f"{self.base_url}{self.tag_url}/{tag_id}",
                auth=(self.consumer_key, self.consumer_secret),
                params={"force": True},
            )

            self.prompt_on_screen(f"tag deleted: {response}")

            return response

        except Exception as exp:
            self.prompt_on_screen(f"delete_tag_by_tag_id: {exp}")


def test():
    WoocommerceTag().get_all_tags()
    WoocommerceTag().resolve_or_upload(name="hahaha")
