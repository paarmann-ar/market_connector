from apis.ebay_api.config.ebay_api_config import (
    EbayApiConfig,
)
from apis.ebay_api.models.search_in_ebay_model import SearchInEbayModel
from apis.ebay_api.core.base_ebay_api import BaseEbayApi
from apis.ebay_api.services.ebay_category import EbayCategory
from apis.ebay_api.services.ebay_product import EbayProduct
from apis.ebay_api.services.ebay_token_api import EbayTokenApi
from toolboxs.decorators import singleton

# --
# ...
# --


@singleton
class EbayApi(BaseEbayApi):
    def __init__(self, **kwargs) -> None:

        self.ebay_token_api = EbayTokenApi()
        self.ebay_token_api()

        self.ebay_category = EbayCategory(ebay_token_api=self.ebay_token_api)
        self.category_dict = {}

        self.ebay_product = EbayProduct(ebay_token_api=self.ebay_token_api)

        self.products_list = []
        self.product_detail_list = []

        self.prompt_on_screen(f"{__class__.__name__}, {id(__class__)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return EbayApiConfig().instance.dictionary

    # --
    # ...
    # --

    def refresh_tocken(self) -> str:
        self.ebay_token_api.get_token()

    # --
    # ...
    # --

    def get_ebay_category_id(self, category_name_candidate) -> str:

        try:
            category_id_candidate = {}
            category_tree_id = self.ebay_category.get_default_category_tree_id_with_marketplace_id()

            if category_name_candidate:
                category_tree = self.ebay_category.get_category_tree(
                    category_tree_id=category_tree_id
                )

                self.recursive_category(category_node=category_tree)

                for category_id, category_name in self.category_dict.items():
                    if category_name == category_name_candidate:
                        category_id_candidate[int(category_id)] = category_name

                self.prompt_on_screen(f"category id: {category_id_candidate}")

                return category_id_candidate

            else:
                return {category_tree_id: "root"}

        except Exception as exp:
            print(f"get_ebay_category_id: {exp}")

    # --
    # ...
    # --

    def recursive_category(self, category_node: dict):
        if "childCategoryTreeNodes" not in category_node:
            self.category_dict.update(
                {category_node["category"]["categoryId"]: category_node["category"]["categoryName"]}
            )
            return

        for child in category_node["childCategoryTreeNodes"]:
            self.recursive_category(category_node=child)

    # --
    # ...
    # --

    def get_all_product_ids(self, category_name_candidate, filter_product, q) -> str:

        try:
            category_id_dict: dict = self.get_ebay_category_id(
                category_name_candidate=category_name_candidate
            )

            for category_id in category_id_dict.keys():
                self.products_list.append(
                    self.ebay_product.get_product_ids_with_category_id(
                        category_id=category_id, filter_product=filter_product, q=q
                    )
                )

            rows = []
            for key, value in self.products_list[0].items():
                row = {"id": key, **value}
                rows.append(row)

            self.csv.operation(mode="w", file_name="ebay_item_summaries.csv", data=rows)

        except Exception as exp:
            print(f"get_all_product_ids: {exp}")

    # --
    # ...
    # --

    def get_product_with_product_id(self, product_id) -> str:

        try:
            self.ebay_product.get_product_with_product_id(product_id=product_id)

        except Exception as exp:
            print(f"get_product_with_product_id: {exp}")

    # --
    # ...
    # --

    def get_all_data_of_product_with_product_id_from_products_list(self) -> str:

        try:
            for product_id in self.products_list[0].keys():
                self.product_detail_list.append(
                    self.ebay_product.get_product_with_product_id(product_id=product_id)
                )

            self.csv.operation(
                mode="w", file_name="ebay_product_detail.csv", data=self.product_detail_list
            )

        except Exception as exp:
            print(f"get_all_data_of_product_with_product_id_from_products_list: {exp}")

    # --
    # ...
    # --

    def fetch_product_from_ebay_by_search_in_ebay_model(
        self, search_in_ebay_model: SearchInEbayModel
    ):
        search_in_ebay_model = search_in_ebay_model.to_dict()

        self.get_all_product_ids(
            category_name_candidate=search_in_ebay_model.get("category_name_candidate"),
            filter_product=search_in_ebay_model.get("filter_product"),
            q=search_in_ebay_model.get("q"),
        )

        self.get_all_data_of_product_with_product_id_from_products_list()


def test():
    EbayApi().get_all_product_ids(
        category_name_candidate="Sonstige Sensoren",
        filter_product="conditions:{NEW},deliveryCountry:DE",
        q="Lambdasonde",
    )
    EbayApi().get_all_data_of_product_with_product_id_from_products_list()
