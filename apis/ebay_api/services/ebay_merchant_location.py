from typing import Any

from apis.ebay_api.config.ebay_api_config import (
    EbayApiConfig,
)
from apis.ebay_api.core.base_ebay_api import BaseEbayApi
from apis.ebay_api.models.inventory.inventory_location_model import InventoryLocationModel

# --
# ...
# --


class EbayMerchantLocation(BaseEbayApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.ebay_inventory_api = self.config_dictionary.get("ebay_inventory_api")
        self.merchant_location_url = self.config_dictionary.get("merchant_location_url")

        self.marketplace_id = self.config_dictionary.get("marketplace_id")
        self.marketplace = self.config_dictionary.get("marketplace")

        self.products = {}

        self.ebay_token_api = kwargs.get("ebay_token_api", None)

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    #  --
    #  ...
    #  --

    @classmethod
    def get_config_dictionary(cls):
        return EbayApiConfig().get_dictionary()

    #  --
    #  ...
    #  --

    def get_ebay_merchant_location_by_inventory_location_model(
        self, inventory_location_model: InventoryLocationModel, marketplace_id: str = ""
    ) -> InventoryLocationModel:

        try:
            if marketplace_id == "":
                marketplace_id = self.marketplace_id

            self.ebay_token_api.get_user_token()
            ebay_access_token = self.ebay_token_api.ebay_user_token

            response = self.request(
                method="get",
                url=f"{self.ebay_inventory_api}{self.merchant_location_url}/{inventory_location_model.merchant_location_key}",
                headers={
                    "Authorization": f"Bearer {ebay_access_token}",
                    "X-EBAY-C-MARKETPLACE-ID": f"{marketplace_id}",
                    "Content-Language": "de-DE",
                },
            )

            self.prompt_on_screen(f"get_ebay_merchant_location_by_inventory_location_model:{response['location']}")

            inventory_location_model = InventoryLocationModel(**response)

            return inventory_location_model

        except Exception as exp:
            self.prompt_on_screen(f"get_ebay_merchant_location_by_inventory_location_model: {exp}")

    #  --
    #  ...
    #  --

    def get_ebay_merchants_location(self, marketplace_id: str = "") -> Any:

        try:
            if marketplace_id == "":
                marketplace_id = self.marketplace_id

            self.ebay_token_api.get_user_token()
            ebay_access_token = self.ebay_token_api.ebay_user_token

            response = self.request(
                method="get",
                url=f"{self.ebay_inventory_api}{self.merchant_location_url}",
                headers={
                    "Authorization": f"Bearer {ebay_access_token}",
                    "X-EBAY-C-MARKETPLACE-ID": f"{marketplace_id}",
                    "Content-Language": "de-DE",
                },
            )

            self.prompt_on_screen(f"get_ebay_merchants_location:{response.get('locations')[0]['merchantLocationKey']}")
            inventory_location_model = InventoryLocationModel(**response.get("locations")[0])
            return inventory_location_model

        except Exception as exp:
            self.prompt_on_screen(f"get_ebay_merchants_location: {exp}")

    #  --
    #  ...
    #  --

    def create_ebay_merchant_location(self, inventory_location_model: InventoryLocationModel, marketplace_id: str = "") -> bool:

        try:
            if marketplace_id == "":
                marketplace_id = self.marketplace_id

            self.ebay_token_api.get_user_token()
            ebay_access_token = self.ebay_token_api.ebay_user_token

            json = inventory_location_model.to_payload()

            response = self.request(
                method="post",
                url=f"{self.ebay_inventory_api}{self.merchant_location_url}/{inventory_location_model.name}",
                headers={
                    "Authorization": f"Bearer {ebay_access_token}",
                    "X-EBAY-C-MARKETPLACE-ID": f"{marketplace_id}",
                    "Content-Language": "de-DE",
                },
                json=json,
            )

            self.prompt_on_screen(f"create_ebay_merchant_location: {response}")

            return response

        except Exception as exp:
            self.prompt_on_screen(f"create_ebay_merchant_location: {exp}")
