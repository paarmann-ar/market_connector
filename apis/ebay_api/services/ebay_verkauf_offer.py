from typing import Any

from apis.ebay_api.config.ebay_api_config import (
    EbayApiConfig,
)
from apis.ebay_api.core.base_ebay_api import BaseEbayApi
from apis.ebay_api.models.offer.offer_ebay_model import OfferEbayModel

# --
# ...
# --


class EbayVerkaufOffer(BaseEbayApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.ebay_inventory_api = self.config_dictionary.get("ebay_inventory_api")
        self.inventory_api_offer_url = self.config_dictionary.get("inventory_api_offer_url")

        self.marketplace_id = self.config_dictionary.get("marketplace_id")
        self.marketplace = self.config_dictionary.get("marketplace")

        self.products = {}

        self.ebay_token_api = kwargs.get("ebay_token_api", None)

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return EbayApiConfig().get_dictionary()

    # --
    # ...
    # --

    def create_offer_ebay(self, offer_ebay_model: OfferEbayModel, marketplace_id: str = "") -> str:

        try:
            if marketplace_id == "":
                marketplace_id = self.marketplace_id

            self.ebay_token_api.get_user_token()
            ebay_access_token = self.ebay_token_api.ebay_user_token

            json = offer_ebay_model.to_dict()

            response = self.request(
                method="post",
                url=f"{self.ebay_inventory_api}{self.inventory_api_offer_url}",
                headers={
                    "Authorization": f"Bearer {ebay_access_token}",
                    "X-EBAY-C-MARKETPLACE-ID": f"{marketplace_id}",
                    "Content-Language": "de-DE",
                },
                json=json,
            )

            self.prompt_on_screen(f"create_offer_ebay: {response}")

            return response.get("offerId")

        except Exception as exp:
            self.prompt_on_screen(f"create_offer_ebay: {exp}")

    # --
    # ...
    # --

    def get_offer_ebay_by_sku(self, sku: str, marketplace_id: str = "") -> OfferEbayModel:

        try:
            if marketplace_id == "":
                marketplace_id = self.marketplace_id

            self.ebay_token_api.get_user_token()
            ebay_access_token = self.ebay_token_api.ebay_user_token

            response = self.request(
                method="get",
                url=f"{self.ebay_inventory_api}{self.inventory_api_offer_url}/?sku={sku}",
                headers={
                    "Authorization": f"Bearer {ebay_access_token}",
                    "X-EBAY-C-MARKETPLACE-ID": f"{marketplace_id}",
                    "Content-Language": "de-DE",
                },
            )

            self.prompt_on_screen(f"get_offer_ebay_by_sku: {response.get('offers')}")

            offer_ebay_model = OfferEbayModel(**response)

            return offer_ebay_model

        except AttributeError:
            self.prompt_on_screen(f"I have no offer for this sku: {sku}")
            return None

        except Exception as exp:
            self.prompt_on_screen(f"get_offer_ebay_by_sku: {exp}")

    # --
    # ...
    # --

    def get_offer_status_ebay_by_offer_id(self, offer_id: str = "") -> str:

        try:
            self.ebay_token_api.get_user_token()
            ebay_access_token = self.ebay_token_api.ebay_user_token

            response = self.request(
                method="get",
                url=f"{self.ebay_inventory_api}{self.inventory_api_offer_url}/{offer_id}",
                headers={
                    "Authorization": f"Bearer {ebay_access_token}",
                    "Content-Language": "de-DE",
                },
            )

            self.prompt_on_screen(f"get_offer_status_ebay_by_offer_id: {response.get('status')}")

            return response.get("status")

        except Exception as exp:
            self.prompt_on_screen(f"get_offer_status_ebay_by_offer_id: {exp}")

    # --
    # ...
    # --

    def get_listing_fees_on_ebay(self, sku: str, offer_id: str, marketplace_id: str = "") -> Any:

        try:
            if marketplace_id == "":
                marketplace_id = self.marketplace_id

            self.ebay_token_api.get_user_token()
            ebay_access_token = self.ebay_token_api.ebay_user_token

            response = self.request(
                method="post",
                url=f"{self.ebay_inventory_api}{self.inventory_api_offer_url}/get_listing_fees",
                headers={
                    "Authorization": f"Bearer {ebay_access_token}",
                    "X-EBAY-C-MARKETPLACE-ID": f"{marketplace_id}",
                    "Content-Language": "de-DE",
                },
                json={"offers": [{"offerId": offer_id}]},
            )

            self.prompt_on_screen(f"get_listing_fees_on_ebay: {response.get('feeSummaries')[0].get('fees')}")

            return response.get("feeSummaries")[0].get("fees")

        except Exception as exp:
            self.prompt_on_screen(f"get_listing_fees_on_ebay: {exp}")

    # --
    # ...
    # --

    def publish_offer_ebay_by_offer_id(self, offer_id: str = "") -> str:

        try:
            return
            self.ebay_token_api.get_user_token()
            ebay_access_token = self.ebay_token_api.ebay_user_token

            response = self.request(
                method="post",
                url=f"{self.ebay_inventory_api}{self.inventory_api_offer_url}/{offer_id}/publish",
                headers={
                    "Authorization": f"Bearer {ebay_access_token}",
                    "Content-Language": "de-DE",
                },
            )

            self.prompt_on_screen(f"publish_offer_ebay_by_offer_id: {response.get('status')}")

            return response.get("status")

        except Exception as exp:
            self.prompt_on_screen(f"publish_offer_ebay_by_offer_id: {exp}")
