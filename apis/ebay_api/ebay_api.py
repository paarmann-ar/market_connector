from apis.ebay_api.config.ebay_api_config import (
    EbayApiConfig,
)
from apis.ebay_api.core.base_ebay_api import BaseEbayApi
from apis.ebay_api.models.browse.product_ebay_model import ProductEbayModel
from apis.ebay_api.models.browse.product_summery_ebay_model import ProductSummeryEbayModel
from apis.ebay_api.models.search_in_ebay_model import SearchInEbayModel
from apis.ebay_api.services.ebay_category import EbayCategory
from apis.ebay_api.services.ebay_product import EbayProduct
from apis.ebay_api.services.ebay_token_api import EbayTokenApi
from apis.ebay_api.services.ebay_inventory import EbayInventory
from apis.ebay_api.adapters.product_to_inventory_adapter import ProductToInventoryAdapter
from apis.ebay_api.adapters.inventory_to_offer_adapter import InventoryToOfferAdapter
from apis.ebay_api.models.offer.offer_ebay_config import OfferEbayConfig
from apis.ebay_api.models.inventory.inventory_location_model import InventoryLocationModel


# --
# ...
# --


class EbayApi(BaseEbayApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.ebay_token_api = EbayTokenApi()

        self.ebay_category = EbayCategory(ebay_token_api=self.ebay_token_api)
        self.category_dict = {}

        self.ebay_product = EbayProduct(ebay_token_api=self.ebay_token_api)
        self.ebay_inventory = EbayInventory(ebay_token_api=self.ebay_token_api)

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
            self.ebay_product.get_product_ebay_model_with_legacy_item_id(legacy_item_id=legacy_item_id)

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

                product_ebay_model.additionalImages = ProductEbayModel.parse_images(product_summery_ebay_model.additionalImages)

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

    # --
    # ...
    # --

    def pipeline_create_ebay_offer(self, product_ebay_model: ProductEbayModel, marketplace_id: str, quantity: int = 1) -> None:

        inventory_product_model = ProductToInventoryAdapter.adapt(
            product=product_ebay_model,
            quantity=quantity,
        )

        offer = self.ebay_inventory.get_offer_ebay_by_sku(sku=inventory_product_model.sku)

        self.ebay_inventory.create_ebay_inventory(inventory_product_model, marketplace_id=marketplace_id)
        inventory_product_model = self.ebay_inventory.get_ebay_inventory_by_sku(
            inventory_product_model=inventory_product_model, marketplace_id=marketplace_id
        )

        inventory_location_model = InventoryLocationModel(
            merchant_location_key="My Warehouse",
            locationTypes=["WAREHOUSE"],
            location={"address": {"addressLine1": "Brückstraße 92", "city": "Erkelenz", "postalCode": "41812", "country": "DE"}},
        )

        inventory_location_model = self.ebay_inventory.get_ebay_merchants_location(marketplace_id=marketplace_id)
        inventory_location_model = self.ebay_inventory.get_ebay_merchant_location_by_inventory_location_model(
            inventory_location_model=inventory_location_model, marketplace_id=marketplace_id
        )
        # self.ebay_inventory.create_ebay_merchant_location(inventory_location_model=inventory_location_model, marketplace_id=marketplace_id)

        offer_ebay_config = OfferEbayConfig(
            marketplace_id=marketplace_id,
            merchant_location_key=inventory_location_model.merchant_location_key,
            category_id="123456",
            fulfillment_policy_id="123456789",
            payment_policy_id="987654321",
            return_policy_id="555555555",
            currency="EUR",
        )

        offer_ebay_model = InventoryToOfferAdapter.adapt(
            inventory_product_model=inventory_product_model, offer_ebay_config=offer_ebay_config
        )

        offer_id = self.ebay_inventory.create_offer_ebay(offer_ebay_model=offer_ebay_model)
        self.ebay_inventory.get_offer_status_ebay_by_offer_id(offer_id=offer_id)
        self.ebay_inventory.get_listing_fees_on_ebay(sku=offer_ebay_model.sku, offer_id=offer_id, marketplace_id=marketplace_id)
