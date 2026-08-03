from apis.ebay_api.config.ebay_api_config import (
    EbayApiConfig,
)
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

    def get_products(
        self, category_id, filter_product, q, offset, limit=200, marketplace=""
    ):

        try:
            if marketplace == "":
                marketplace = self.marketplace

            self.ebay_token_api()
            self.ebay_access_token = self.ebay_token_api.ebay_access_token

            url = f"{self.base_url}{self.products_url}?limit={limit}&offset={offset}"
            if category_id:
                url = url + f"&category_ids={category_id}"

            if filter_product:
                url = url + f"&filter={filter_product}"

            if q:
                url = url + f"&q={q}"

            response = self.request(
                method="get",
                url=url,
                headers={
                    "Authorization": f"Bearer {self.ebay_access_token}",
                    "X-EBAY-C-MARKETPLACE-ID": f"{marketplace}",
                },
            )

            self.prompt_on_screen(f"get_products: {response}")

            return response["itemSummaries"], response["offset"], response["total"]

        except Exception as exp:
            print(f"get_products: {exp}")

    # --
    # ...
    # --

    def get_product_ids_with_category_id(
        self, category_id, filter_product, q, marketplace=""
    ):

        try:
            if marketplace == "":
                marketplace = self.marketplace

            offset = 0

            while True:
                item_summaries, offset, total = self.get_products(
                    category_id=category_id,
                    offset=offset,
                    filter_product=filter_product,
                    q=q,
                )
                offset += 200

                for product in item_summaries:
                    self.products.update({product["itemId"]: product})

                if offset >= total:
                    break

            return self.products

        except Exception as exp:
            print(f"get_product_ids_with_category_id: {exp}")

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

            self.prompt_on_screen(f"product: {response}")

            return response

        except Exception as exp:
            print(f"get_product_with_product_id: {exp}")
