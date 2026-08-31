from apis.woocommerce_api.config.woocommerce_api_config import (
    WoocommerceApiConfig,
)
from apis.woocommerce_api.core.base_woocommerce_api import (
    BaseWoocommerceApi,
)
import html
from apis.woocommerce_api.models.woocommerce_attribute_model import WoocommerceAttributeModel
from apis.woocommerce_api.models.woocommerce_attribute_model import WoocommerceAttributeTermModel
from typing import Optional
# --
# ...
# --


class WoocommerceAttribute(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.base_url = self.config_dictionary.get("base_url")
        self.wp_media_url = self.config_dictionary.get("wp_media_url")

        self.consumer_key = self.config_dictionary.get("consumer_key")
        self.consumer_secret = self.config_dictionary.get("consumer_secret")

        self.wp_user = self.config_dictionary.get("wp_user")
        self.wp_password = self.config_dictionary.get("wp_password")

        self.attribute_url = self.config_dictionary.get("attribute_url")

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    #  --
    #  ...
    #  --

    @classmethod
    def get_config_dictionary(cls):
        return WoocommerceApiConfig().get_dictionary()

    #  --
    #  ...
    #  --

    def __call__(self, attribute_id) -> str:
        return self.get_attribute_by_id(attribute_id)

    # --
    # ...
    # --

    def get_attribute_by_id(
        self,
        attribute_id: int,
    ):

        try:
            response = self.request(
                method="get",
                url=f"{self.base_url}{self.attribute_url}/{attribute_id}",
                auth=(self.consumer_key, self.consumer_secret),
            )

            if not response:
                return None

            return WoocommerceAttributeModel.from_api(response)

        except Exception as exp:
            self.prompt_on_screen(f"get_attribute_by_id: {exp}")

            return None

    # --
    # ...
    # --

    def get_attribute_by_name(
        self,
        name: str,
        record_per_page: int = 100,
    ):

        try:
            response = self.request(
                method="get",
                url=f"{self.base_url}{self.attribute_url}",
                auth=(self.consumer_key, self.consumer_secret),
                params={
                    "per_page": record_per_page,
                },
            )

            if not response:
                return None

            normalized_name = html.unescape(name).strip().lower()

            for attribute in response:
                attribute_name = html.unescape(attribute["name"]).strip().lower()

                if attribute_name == normalized_name:
                    return WoocommerceAttributeModel.from_api(attribute)

            return None

        except Exception as exp:
            self.prompt_on_screen(f"get_attribute_by_name: {exp}")

            return None

    # --
    # ...
    # --

    def get_all_attributes(
        self,
        record_per_page: int = 100,
    ):

        try:
            response = self.request(
                method="get",
                url=f"{self.base_url}{self.attribute_url}",
                auth=(self.consumer_key, self.consumer_secret),
                params={
                    "per_page": record_per_page,
                },
            )

            if not response:
                return []

            return [WoocommerceAttributeModel.from_api(attribute) for attribute in response]

        except Exception as exp:
            self.prompt_on_screen(f"get_all_attributes: {exp}")

            return []

    # --
    # ...
    # --

    def upload_attribute(
        self,
        attribute_model: WoocommerceAttributeModel,
    ):

        try:
            response = self.request(
                method="post",
                url=f"{self.base_url}{self.attribute_url}",
                auth=(self.consumer_key, self.consumer_secret),
                json=attribute_model.to_dict(),
            )

            self.prompt_on_screen(f"attribute to upload: {response}")

            return WoocommerceAttributeModel.from_api(response)

        except Exception as exp:
            self.prompt_on_screen(f"upload_attribute: {exp}")

            return None

    # --
    # ...
    # --

    def resolve_or_upload(
        self,
        attribute_model: WoocommerceAttributeModel,
    ) -> Optional[WoocommerceAttributeModel]:

        existing = self.get_attribute_by_name(attribute_model.name)

        if existing:
            return existing

        return self.upload_attribute(attribute_model)

    # ==================================================
    # TERMS
    # ==================================================

    def get_term_by_name(
        self,
        attribute_id: int,
        name: str,
        record_per_page: int = 100,
    ):

        try:
            response = self.request(
                method="get",
                url=f"{self.base_url}{self.attribute_url}/{attribute_id}/terms",
                auth=(
                    self.consumer_key,
                    self.consumer_secret,
                ),
                params={
                    "per_page": record_per_page,
                },
            )

            if not response:
                return None

            normalized_name = html.unescape(name).strip().lower()

            for term in response:
                term_name = html.unescape(term["name"]).strip().lower()

                if term_name == normalized_name:
                    return WoocommerceAttributeTermModel.from_api(term)

            return None

        except Exception as exp:
            self.prompt_on_screen(f"get_term_by_name: {exp}")

            return None

    # --
    # ...
    # --

    def get_all_terms(
        self,
        attribute_id: int,
        record_per_page: int = 100,
    ):

        try:
            response = self.request(
                method="get",
                url=f"{self.base_url}{self.attribute_url}/{attribute_id}/terms",
                auth=(
                    self.consumer_key,
                    self.consumer_secret,
                ),
                params={
                    "per_page": record_per_page,
                },
            )

            if not response:
                return []

            return [WoocommerceAttributeTermModel.from_api(term) for term in response]

        except Exception as exp:
            self.prompt_on_screen(f"get_all_terms: {exp}")

            return []

    # --
    # ...
    # --

    def upload_term(
        self,
        attribute_id: int,
        term_model: WoocommerceAttributeTermModel,
    ):

        try:
            response = self.request(
                method="post",
                url=f"{self.base_url}{self.attribute_url}/{attribute_id}/terms",
                auth=(
                    self.consumer_key,
                    self.consumer_secret,
                ),
                json=term_model.to_dict(),
            )

            self.prompt_on_screen(f"attribute term to upload: {response}")

            return WoocommerceAttributeTermModel.from_api(response)

        except Exception as exp:
            self.prompt_on_screen(f"upload_term: {exp}")

            return None

    # --
    # ...
    # --

    def resolve_or_upload_term(
        self,
        attribute_id: int,
        term_model: WoocommerceAttributeTermModel,
    ):

        existing = self.get_term_by_name(
            attribute_id=attribute_id,
            name=term_model.name,
        )

        if existing:
            return existing

        return self.upload_term(
            attribute_id=attribute_id,
            term_model=term_model,
        )
