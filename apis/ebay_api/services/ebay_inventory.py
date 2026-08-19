from apis.ebay_api.config.ebay_api_config import (
    EbayApiConfig,
)
from typing import Optional, Any

from apis.ebay_api.core.base_ebay_api import BaseEbayApi
from apis.ebay_api.models.browse.product_ebay_model import ProductEbayModel
from apis.ebay_api.models.inventory.inventory_product_model import InventoryProductModel
from apis.ebay_api.models.offer.offer_ebay_model import OfferEbayModel
from toolboxs.xml_tool import XmlTool
from apis.ebay_api.models.inventory.inventory_location_model import InventoryLocationModel

# --
# ...
# --


class EbayInventory(BaseEbayApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.ebay_trading_api = self.config_dictionary.get("ebay_trading_api")

        self.ebay_inventory_api = self.config_dictionary.get("ebay_inventory_api")
        self.inventory_api_item_url = self.config_dictionary.get("inventory_api_item_url")
        self.inventory_api_offer_url = self.config_dictionary.get("inventory_api_offer_url")
        self.merchant_location_url = self.config_dictionary.get("merchant_location_url")

        self.marketplace_id = self.config_dictionary.get("marketplace_id")
        self.marketplace = self.config_dictionary.get("marketplace")

        self.product_name = "laptop"
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

    def get_sku_with_item_id(self, item_id: str, marketplace_id: str = "") -> ProductEbayModel:

        try:
            if marketplace_id == "":
                marketplace_id = self.marketplace_id

            self.ebay_token_api.get_user_token()
            ebay_access_token = self.ebay_token_api.ebay_user_token

            response = self.request(
                method="post",
                url=self.ebay_trading_api,
                headers={
                    "X-EBAY-API-CALL-NAME": "GetItem",
                    "X-EBAY-API-SITEID": "77",
                    "X-EBAY-API-COMPATIBILITY-LEVEL": "1231",
                    "X-EBAY-API-IAF-TOKEN": ebay_access_token,
                    "Content-Type": "text/xml",
                },
                data=f"""<?xml version="1.0" encoding="utf-8"?>
                <GetItemRequest xmlns="urn:ebay:apis:eBLBaseComponents">
                    <RequesterCredentials>
                        <eBayAuthToken>{ebay_access_token}</eBayAuthToken>
                    </RequesterCredentials>
                    <ItemID>{item_id}</ItemID>
                    <DetailLevel>ReturnAll</DetailLevel>
                </GetItemRequest>
                """.encode(),
            )

            sku = XmlTool.get_item(context=response.get("cntent"), key="SKU")

            self.prompt_on_screen(f"get_product_with_sku: item_id={item_id}, SKU: {sku}")
            return ProductEbayModel(**response)

        except Exception as exp:
            self.prompt_on_screen(f"get_product_with_sku: {exp}")

    # --
    # ...
    # --

    def create_ebay_inventory(self, inventory_product_model: InventoryProductModel, marketplace_id: str = "") -> bool:

        try:
            if marketplace_id == "":
                marketplace_id = self.marketplace_id

            self.ebay_token_api.get_user_token()
            ebay_access_token = self.ebay_token_api.ebay_user_token

            response = self.request(
                method="put",
                url=f"{self.ebay_inventory_api}{self.inventory_api_item_url}/{inventory_product_model.sku}",
                headers={
                    "Authorization": f"Bearer {ebay_access_token}",
                    "X-EBAY-C-MARKETPLACE-ID": f"{marketplace_id}",
                    "Content-Language": "de-DE",
                },
                data=inventory_product_model.to_json(),
            )

            self.prompt_on_screen(f"create_ebay_inventory:{response}")

            return response

        except Exception as exp:
            self.prompt_on_screen(f"get_product_with_sku: {exp}")

    # --
    # ...
    # --

    def get_ebay_inventory_by_sku(self, inventory_product_model: InventoryProductModel, marketplace_id: str = "") -> InventoryProductModel:

        try:
            if marketplace_id == "":
                marketplace_id = self.marketplace_id

            self.ebay_token_api.get_user_token()
            ebay_access_token = self.ebay_token_api.ebay_user_token

            response = self.request(
                method="get",
                url=f"{self.ebay_inventory_api}{self.inventory_api_item_url}/{inventory_product_model.sku}",
                headers={
                    "Authorization": f"Bearer {ebay_access_token}",
                    "X-EBAY-C-MARKETPLACE-ID": f"{marketplace_id}",
                    "Content-Language": "de-DE",
                },
            )

            self.prompt_on_screen(f"get_ebay_inventory_by_sku: {response}")

            inventory_product_model = InventoryProductModel(**response)

            return inventory_product_model

        except Exception as exp:
            self.prompt_on_screen(f"get_ebay_inventory_by_sku: {exp}")

    # --
    # ...
    # --

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

    # --
    # ...
    # --

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

    # --
    # ...
    # --

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

            return response

        except AttributeError as exp:
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

    def get_listing_fees_on_ebay(self, sku: str, offer_id: str, marketplace_id: str = "") -> bool:

        try:
            if marketplace_id == "":
                marketplace_id = self.marketplace_id

            self.ebay_token_api.get_user_token()
            ebay_access_token = self.ebay_token_api.ebay_user_token

            response = self.request(
                method="get",
                url=f"{self.ebay_inventory_api}{self.inventory_api_offer_url}/get_listing_fees",
                headers={
                    "Authorization": f"Bearer {ebay_access_token}",
                    "X-EBAY-C-MARKETPLACE-ID": f"{marketplace_id}",
                    "Content-Language": "de-DE",
                },
                json={"offers": [{"offerId": offer_id}]},
            )

            self.prompt_on_screen(f"get_listing_fees_on_ebay: {response.get('offers')}")

            return response

        except Exception as exp:
            self.prompt_on_screen(f"get_listing_fees_on_ebay: {exp}")

    # --
    # ...
    # --

    def get_all_skus_on_ebay(self, marketplace_id: str = "") -> bool:

        try:
            if marketplace_id == "":
                marketplace_id = self.marketplace_id

            self.ebay_token_api.get_user_token()
            ebay_access_token = self.ebay_token_api.ebay_user_token

            response = self.request(
                method="get",
                url=f"{self.ebay_inventory_api}/inventory_item",
                headers={
                    "Authorization": f"Bearer {ebay_access_token}",
                    "X-EBAY-C-MARKETPLACE-ID": f"{marketplace_id}",
                    "Content-Language": "de-DE",
                },
            )

            self.prompt_on_screen(f"get_allskus_on_ebay: {response.get('inventoryItems')}")

            return response

        except Exception as exp:
            self.prompt_on_screen(f"get_allskus_on_ebay: {exp}")





    def hi(self):

        import requests
        self.ebay_token_api.get_user_token()
        ebay_access_token = self.ebay_token_api.ebay_user_token
        url = "https://api.ebay.com/sell/inventory/v1/offer/get_listing_fees"

        headers = {
            "Authorization": f"Bearer {ebay_access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-EBAY-C-MARKETPLACE-ID": "EBAY_DE",
            "Content-Language": "de-DE",
        }

        payload = {
            "offers": [
                {
                    "offerId": "241005937011"
                }
            ]
        }

        r = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=(12, 120),
        )

        print("STATUS:", r.status_code)
        print("TEXT:", r.text)