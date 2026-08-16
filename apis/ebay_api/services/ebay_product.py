from apis.ebay_api.config.ebay_api_config import (
    EbayApiConfig,
)
from apis.ebay_api.models.search_in_ebay_model import SearchInEbayModel
from apis.ebay_api.core.base_ebay_api import BaseEbayApi
from apis.ebay_api.models.product_summery_ebay_model import ProductSummeryEbayModel
from apis.ebay_api.models.product_ebay_model import ProductEbayModel



# --
# ...
# --


class EbayProduct(BaseEbayApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.base_url = self.config_dictionary.get("base_url")
        self.products_url = self.config_dictionary.get("products_url")
        self.product_url = self.config_dictionary.get("product_url")

        self.inventory_item_url = self.config_dictionary.get("inventory_item_url")

        self.marketplace_id = self.config_dictionary.get("marketplace_id")
        self.marketplace = self.config_dictionary.get("marketplace")

        self.product_name = "laptop"
        self.products = {}

        self.ebay_token_api = kwargs.get("ebay_token_api", None)
        self.ebay_access_token = self.ebay_token_api.ebay_access_token

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

    def get_product_summery_ebay_models(self, search_in_ebay_model: SearchInEbayModel, offset=0)-> list[ProductSummeryEbayModel]:

        try:
            self.ebay_token_api()
            self.ebay_access_token = self.ebay_token_api.ebay_access_token

            search_in_ebay_model.generate_filter()

            params = {
                "limit": 200,
                "offset": offset,
                "filter": search_in_ebay_model.filter,
                "q": search_in_ebay_model.q,
            }

            response = self.request(
                method="get",
                url=f"{self.base_url}{self.products_url}",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.ebay_access_token}",
                    "X-EBAY-C-MARKETPLACE-ID": f"{search_in_ebay_model.marketplace}",
                },
                params=params,
            )

            product_summery_ebay_models :list[ ProductSummeryEbayModel] = []

            for itemSummary in response["itemSummaries"]:
               product_summery_ebay_models.append( ProductSummeryEbayModel(**itemSummary))

            return product_summery_ebay_models

        except Exception as exp:
            self.prompt_on_screen(f"get_products: {exp}")

    # --
    # ...
    # --

    def get_product_ebay_model_with_legacy_item_id(self, legacy_item_id: str, marketplace_id:str="")->ProductEbayModel:

        try:
            # in endpoint shortDescription ro nemideh shabih be ProductEbayModel hast
            if marketplace_id == "":
                marketplace_id = self.marketplace_id

            self.ebay_token_api()
            self.ebay_access_token = self.ebay_token_api.ebay_access_token

            response = self.request(
                method="get",
                url=f"{self.base_url}{self.product_url}/get_item_by_legacy_id?legacy_item_id={legacy_item_id}",
                headers={
                    "Authorization": f"Bearer {self.ebay_access_token}",
                    "X-EBAY-C-MARKETPLACE-ID": f"{marketplace_id}",
                },
            )

            self.prompt_on_screen(f"get_product_ebay_model_with_legacy_item_id: legacy_item_id={legacy_item_id}, title:{response.get('title')}")
            return ProductEbayModel(**response)

        except Exception as exp:
            self.prompt_on_screen(f"get_product_with_legacy_item_id: {exp}")

    # --
    # ...
    # --

    def get_product_ebay_model_with_item_id(self, product_item_id: str, marketplace_id:str="")->ProductEbayModel:

        try:
            if marketplace_id == "":
                marketplace_id = self.marketplace_id

            self.ebay_token_api()
            self.ebay_access_token = self.ebay_token_api.ebay_access_token

            response = self.request(
                method="get",
                url=f"{self.base_url}{self.product_url}/{product_item_id}",
                headers={
                    "Authorization": f"Bearer {self.ebay_access_token}",
                    "X-EBAY-C-MARKETPLACE-ID": f"{marketplace_id}",
                },
            )

            self.prompt_on_screen(f"get_product_ebay_model_with_item_id: product_item_id={product_item_id}, title: {response.get('title')}")
            return ProductEbayModel(**response)

        except Exception as exp:
            self.prompt_on_screen(f"get_product_ebay_model_with_item_id: {exp}")

    # --
    # ...
    # --
