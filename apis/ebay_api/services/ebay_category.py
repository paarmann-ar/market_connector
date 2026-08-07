from apis.ebay_api.config.ebay_api_config import (
    EbayApiConfig,
)
from apis.ebay_api.core.base_ebay_api import BaseEbayApi

# --
# ...
# --


class EbayCategory(BaseEbayApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.base_url = self.config_dictionary.get("base_url")
        self.taxonomy_url = self.config_dictionary.get("taxonomy_url")

        self.product_name = ""

        self.marketplace_id = self.config_dictionary.get("marketplace_id")
        self.marketplace = self.config_dictionary.get("marketplace")

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

    def get_default_category_tree_id_with_marketplace_id(self, marketplace=""):

        try:
            if marketplace == "":
                marketplace = self.marketplace

            self.ebay_token_api()
            self.ebay_access_token = self.ebay_token_api.ebay_access_token

            response = self.request(
                method="get",
                url=f"{self.base_url}{self.taxonomy_url}/get_default_category_tree_id?marketplace_id={marketplace}",
                headers={
                    "Authorization": f"Bearer {self.ebay_access_token}",
                },
            )

            self.category_tree_id = int(response["categoryTreeId"])

            self.prompt_on_screen(f"Default category tree id: {self.category_tree_id}")

            return self.category_tree_id

        except Exception as exp:
            self.prompt_on_screen(f"get_default_category_tree_id_with_marketplace_id: {exp}")

    # --
    # ...
    # --

    def get_category_tree(self, category_tree_id=""):

        try:
            if category_tree_id == "":
                category_tree_id = self.category_tree_id

            self.ebay_token_api()
            self.ebay_access_token = self.ebay_token_api.ebay_access_token

            response = self.request(
                method="get",
                url=f"{self.base_url}{self.taxonomy_url}/category_tree/{category_tree_id}",
                headers={
                    "Authorization": f"Bearer {self.ebay_access_token}",
                },
            )

            self.category_tree = response["rootCategoryNode"]

            return self.category_tree

        except Exception as exp:
            self.prompt_on_screen(f"get_category_tree: {exp}")
