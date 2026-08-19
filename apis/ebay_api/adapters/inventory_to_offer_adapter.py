from typing import Optional

from apis.ebay_api.models.inventory.inventory_product_model import InventoryProductModel
from apis.ebay_api.models.offer.offer_ebay_model import OfferEbayModel
from apis.ebay_api.models.offer.offer_ebay_config import OfferEbayConfig

# --
# ...
# --


class InventoryToOfferAdapter:
    @staticmethod
    def adapt(
        inventory_product_model: InventoryProductModel,
        offer_ebay_config: OfferEbayConfig,
    ) -> OfferEbayModel:

        listing_policies = {
            "fulfillmentPolicyId": offer_ebay_config.fulfillment_policy_id,
            "paymentPolicyId": offer_ebay_config.payment_policy_id,
            "returnPolicyId": offer_ebay_config.return_policy_id,
        }

        pricing_summary = {
            "price": {
                "value": inventory_product_model.price,
                "currency": offer_ebay_config.currency,
            }
        }

        return OfferEbayModel(
            sku=inventory_product_model.sku,
            marketplaceId=offer_ebay_config.marketplace_id,
            format="FIXED_PRICE",
            categoryId=offer_ebay_config.category_id,
            merchantLocationKey=offer_ebay_config.merchant_location_key,
            availableQuantity=inventory_product_model.quantity,
            listingDescription=inventory_product_model.product.get("description"),
            listingDuration=offer_ebay_config.listing_duration,
            pricingSummary=pricing_summary,
            listingPolicies=listing_policies,
            lotSize=None,
        )
