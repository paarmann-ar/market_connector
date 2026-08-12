from apis.ebay_api.config.ebay_api_config import (
    EbayApiConfig,
)
from apis.ebay_api.models.search_in_ebay_model import SearchInEbayModel
from apis.ebay_api.core.base_ebay_api import BaseEbayApi

# --
# ...
# --


class EbayProduct(BaseEbayApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.base_url = self.config_dictionary.get("base_url")
        self.products_url = self.config_dictionary.get("products_url")
        self.product_url = self.config_dictionary.get("product_url")

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

    def get_products(self, search_in_ebay_model:SearchInEbayModel,offset=0):

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

            self.prompt_on_screen(f"get_products: {response.get('total')}")

            return response["itemSummaries"], response["offset"], response["total"]

        except Exception as exp:
            self.prompt_on_screen(f"get_products: {exp}")

    # --
    # ...
    # --

    def get_product_ids_with_category_id(self, search_in_ebay_model: SearchInEbayModel):

        try:
            offset = 0

            while True:
                item_summaries, offset, total = self.get_products(search_in_ebay_model)
                offset += 200

                for product in item_summaries:
                    self.products.update({product["itemId"]: product})

                if offset >= total:
                    break

            self.products = dict(list(self.products.items())[: search_in_ebay_model.item_to_fetch])
            return self.products

        except Exception as exp:
            self.prompt_on_screen(f"get_product_ids_with_category_id: {exp}")

    # --
    # ...
    # --

    def get_product_with_product_id(self, product_id, marketplace=""):

        try:
            if marketplace == "":
                marketplace = self.marketplace

            self.ebay_token_api()
            self.ebay_access_token = self.ebay_token_api.ebay_access_token

            response = self.request(
                method="get",
                url=f"{self.base_url}{self.product_url}/{product_id}",
                headers={
                    "Authorization": f"Bearer {self.ebay_access_token}",
                    "X-EBAY-C-MARKETPLACE-ID": f"{marketplace}",
                },
            )

            self.prompt_on_screen(f"product: {response.get('title')}")

            return response

        except Exception as exp:
            self.prompt_on_screen(f"get_product_with_product_id: {exp}")
