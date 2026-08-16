from apis.ebay_api.config.ebay_api_config import (
    EbayApiConfig,
)
from apis.ebay_api.core.base_ebay_api import BaseEbayApi
from apis.ebay_api.models.product_ebay_model import ProductEbayModel
from apis.ebay_api.models.product_summery_ebay_model import ProductSummeryEbayModel
from apis.ebay_api.models.search_in_ebay_model import SearchInEbayModel
from apis.ebay_api.services.ebay_category import EbayCategory
from apis.ebay_api.services.ebay_product import EbayProduct
from apis.ebay_api.services.ebay_token_api import EbayTokenApi

# --
# ...
# --


class EbayApi(BaseEbayApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.ebay_token_api = EbayTokenApi()
        self.ebay_token_api()

        self.ebay_category = EbayCategory(ebay_token_api=self.ebay_token_api)
        self.category_dict = {}

        self.ebay_product = EbayProduct(ebay_token_api=self.ebay_token_api)

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

    def refresh_token(self) -> str:
        self.ebay_token_api.get_token()

    # --
    # ...
    # --

    def get_ebay_category_id(self, search_in_ebay_model: SearchInEbayModel) -> str:

        try:
            category_id_candidate = {}
            category_tree_id = self.ebay_category.get_default_category_tree_id_with_marketplace_id(
                marketplace=search_in_ebay_model.marketplace
            )

            if search_in_ebay_model.category_name_candidate:
                self.category_dict.clear()
                category_tree = self.ebay_category.get_category_tree(category_tree_id=category_tree_id)

                self.recursive_category(category_node=category_tree)

                for category_id, category_name in self.category_dict.items():
                    if category_name == search_in_ebay_model.category_name_candidate:
                        category_id_candidate[int(category_id)] = category_name

                self.prompt_on_screen(f"category id: {category_id_candidate}")

                search_in_ebay_model.category_id = category_id_candidate
                return category_id_candidate

            else:
                search_in_ebay_model.category_id = category_tree_id
                return {category_tree_id: "root"}

        except Exception as exp:
            self.prompt_on_screen(f"get_ebay_category_id: {exp}")

    # --
    # ...
    # --

    def recursive_category(self, category_node: dict):
        if "childCategoryTreeNodes" not in category_node:
            self.category_dict.update({category_node["category"]["categoryId"]: category_node["category"]["categoryName"]})
            return

        for child in category_node["childCategoryTreeNodes"]:
            self.recursive_category(category_node=child)

    # --
    # ...
    # --

    def get_product_with_product_id(self, legacy_item_id) -> str:

        try:
            self.ebay_product.get_product_with_legacy_item_id(legacy_item_id=legacy_item_id)

        except Exception as exp:
            self.prompt_on_screen(f"get_product_with_product_id: {exp}")

    # --
    # ...
    # --

    def get_product_ebay_models_with_product_id(self, product_summery_ebay_models: list[ProductSummeryEbayModel]) -> list[ProductEbayModel]:

        try:
            product_ebay_models: list[ProductEbayModel] = []

            for product_summery_ebay_model in product_summery_ebay_models:
                product_ebay_model = self.ebay_product.get_product_ebay_model_with_item_id(
                    product_item_id=product_summery_ebay_model.itemId, marketplace_id=product_summery_ebay_model.listingMarketplaceId
                )

                product_ebay_model.additionalImages = product_summery_ebay_model.additionalImages
                product_ebay_models.append(product_ebay_model)

            self.csv.operation(
                mode="w",
                file_name="ebay_product_detail.csv",
                data=product_ebay_models,
            )

            return product_ebay_models

        except Exception as exp:
            self.prompt_on_screen(f"get_product_ebay_models_with_product_id: {exp}")
            return []

    # --
    # ...
    # --

    def fetch_product_from_ebay_by_search_in_ebay_model(self, search_in_ebay_model: SearchInEbayModel) -> list[ProductEbayModel]:
        if search_in_ebay_model.legacy_item_id:
            product_ebay_model = self.ebay_product.get_product_ebay_model_with_legacy_item_id(
                legacy_item_id=search_in_ebay_model.legacy_item_id, marketplace_id=search_in_ebay_model.marketplace_id
            )
            return [product_ebay_model]

        else:
            product_summery_ebay_models = self.ebay_product.get_product_summery_ebay_models(search_in_ebay_model=search_in_ebay_model)
            product_summery_ebay_models = product_summery_ebay_models[: search_in_ebay_model.item_to_fetch]

        return self.get_product_ebay_models_with_product_id(product_summery_ebay_models=product_summery_ebay_models)
