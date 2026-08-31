from apis.ebay_api.adapters.inventory_to_offer_adapter import InventoryToOfferAdapter
from apis.ebay_api.adapters.product_to_inventory_adapter import ProductToInventoryAdapter
from apis.ebay_api.config.ebay_api_config import (
    EbayApiConfig,
)
from apis.ebay_api.core.base_ebay_api import BaseEbayApi
from apis.ebay_api.models.browse.product_ebay_model import ProductEbayModel
from apis.ebay_api.models.inventory.inventory_location_model import InventoryLocationModel
from apis.ebay_api.models.offer.offer_ebay_config import OfferEbayConfig
from apis.ebay_api.models.search_in_ebay_model import SearchInEbayModel
from apis.ebay_api.services.ebay_category import EbayCategory
from apis.ebay_api.services.ebay_inventory import EbayInventory
from apis.ebay_api.services.ebay_merchant_location import EbayMerchantLocation
from apis.ebay_api.services.ebay_product import EbayProduct
from apis.ebay_api.services.ebay_token_api import EbayTokenApi
from apis.ebay_api.services.ebay_verkauf_offer import EbayVerkaufOffer
from apis.ebay_api.services.ebay_verkauf_policys import EbayVerkaufPolicys

# --
# ...
# --


class EbayApi(BaseEbayApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.ebay_token_api = EbayTokenApi()

        self.ebay_category = EbayCategory(ebay_token_api=self.ebay_token_api)

        self.ebay_product = EbayProduct(ebay_token_api=self.ebay_token_api)
        self.ebay_inventory = EbayInventory(ebay_token_api=self.ebay_token_api)

        self.ebay_verkauf_policys = EbayVerkaufPolicys(ebay_token_api=self.ebay_token_api)
        self.ebay_merchant_location = EbayMerchantLocation(ebay_token_api=self.ebay_token_api)
        self.ebay_verkauf_offer = EbayVerkaufOffer(ebay_token_api=self.ebay_token_api)

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

    def pipeline_fetch_product_from_ebay_by_search_in_ebay_model(self, search_in_ebay_model: SearchInEbayModel) -> list[ProductEbayModel]:
        product_ebay_models: list[ProductEbayModel] = []

        if search_in_ebay_model.legacy_item_id:
            product_ebay_model = self.ebay_product.get_product_ebay_model_with_legacy_item_id(
                legacy_item_id=search_in_ebay_model.legacy_item_id, marketplace_id=search_in_ebay_model.marketplace_id
            )
            return [product_ebay_model]

        else:
            product_summery_ebay_models = self.ebay_product.get_product_summery_ebay_models(search_in_ebay_model=search_in_ebay_model)
            product_summery_ebay_models = product_summery_ebay_models[: search_in_ebay_model.item_to_fetch]

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

    #  --
    #  ...
    #  --

    def pipeline_create_ebay_offer(self, product_ebay_model: ProductEbayModel, marketplace_id: str, quantity: int = 1) -> None:
        categoryies_object = self.ebay_category.change_category_between_marketplaces(us_category_path=product_ebay_model.categoryIdPath)

        product_ebay_model.categoryId = categoryies_object.get("de_cat_id")
        product_ebay_model.categoryIdPath = categoryies_object.get("de_cat_path")
        product_ebay_model.categoryPath = categoryies_object.get("de_cat_name_path")

        inventory_product_model = ProductToInventoryAdapter.adapt(
            product=product_ebay_model,
            quantity=quantity,
        )

        offer_ebay_model = self.ebay_verkauf_offer.get_offer_ebay_by_sku(sku=inventory_product_model.sku)

        self.ebay_inventory.create_ebay_inventory(inventory_product_model, marketplace_id=marketplace_id)

        inventory_location_model = InventoryLocationModel(
            merchant_location_key="My Warehouse",
            locationTypes=["WAREHOUSE"],
            location={"address": {"addressLine1": "Brückstraße 92", "city": "Erkelenz", "postalCode": "41812", "country": "DE"}},
        )

        inventory_location_model = self.ebay_merchant_location.get_ebay_merchants_location(marketplace_id=marketplace_id)
        inventory_location_model = self.ebay_merchant_location.get_ebay_merchant_location_by_inventory_location_model(
            inventory_location_model=inventory_location_model, marketplace_id=marketplace_id
        )

        fulfillment_policys = self.ebay_verkauf_policys.get_all_fulfillment_policy_on_ebay(marketplace_id=marketplace_id)
        fulfillment_policy_id = fulfillment_policys[0]["fulfillmentPolicyId"]

        zahlung_policys = self.ebay_verkauf_policys.get_all_zahlungs_policy_on_ebay(marketplace_id=marketplace_id)
        zahlungs_policy_id = zahlung_policys[0]["paymentPolicyId"]

        ruckgabe_policys = self.ebay_verkauf_policys.get_all_ruckgabes_policy_on_ebay(marketplace_id=marketplace_id)
        ruckgabe_policy_id = ruckgabe_policys[0]["returnPolicyId"]

        offer_ebay_config = OfferEbayConfig(
            marketplace_id=marketplace_id,
            merchant_location_key=inventory_location_model.merchant_location_key,
            currency=inventory_product_model.price["currency"],
            category_id=product_ebay_model.categoryId,
            fulfillment_policy_id=fulfillment_policy_id,
            payment_policy_id=zahlungs_policy_id,
            return_policy_id=ruckgabe_policy_id,
        )

        offer_ebay_model = InventoryToOfferAdapter.adapt(
            inventory_product_model=inventory_product_model, offer_ebay_config=offer_ebay_config
        )

        offer_id = self.ebay_verkauf_offer.create_offer_ebay(offer_ebay_model=offer_ebay_model)
        self.ebay_verkauf_offer.get_offer_status_ebay_by_offer_id(offer_id=offer_id)
        self.ebay_verkauf_offer.get_listing_fees_on_ebay(sku=offer_ebay_model.sku, offer_id=offer_id, marketplace_id=marketplace_id)
        self.ebay_verkauf_offer.publish_offer_ebay_by_offer_id(offer_id=offer_id)
