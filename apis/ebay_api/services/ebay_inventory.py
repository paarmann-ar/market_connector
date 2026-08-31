from apis.ebay_api.config.ebay_api_config import (
    EbayApiConfig,
)
from apis.ebay_api.core.base_ebay_api import BaseEbayApi
from apis.ebay_api.models.browse.product_ebay_model import ProductEbayModel
from apis.ebay_api.models.inventory.inventory_product_model import InventoryProductModel
from toolboxs.xml_tool import XmlTool

# --
# ...
# --


class EbayInventory(BaseEbayApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.ebay_trading_api = self.config_dictionary.get("ebay_trading_api")

        self.ebay_inventory_api = self.config_dictionary.get("ebay_inventory_api")
        self.inventory_api_item_url = self.config_dictionary.get("inventory_api_item_url")
        self.merchant_location_url = self.config_dictionary.get("merchant_location_url")

        self.marketplace_id = self.config_dictionary.get("marketplace_id")
        self.marketplace = self.config_dictionary.get("marketplace")

        self.product_name = "laptop"
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

    #  --
    #  ...
    #  --

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

    #  --
    #  ...
    #  --

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

    #  --
    #  ...
    #  --

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
