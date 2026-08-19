from dataclasses import dataclass, fields
from typing import Optional
from apis.ebay_api.models.inventory.inventory_location_model import InventoryLocationModel

# --
# ...
# --


@dataclass
class OfferEbayConfig:
    marketplace_id: str
    merchant_location_key: str
    category_id: str

    fulfillment_policy_id: str
    payment_policy_id: str
    return_policy_id: str

    currency: str

    listing_duration: str = "GTC"

    # --
    # ...
    # --

    def __init__(self, **kwargs):

        valid_fields = {field.name for field in fields(self)}

        for key, value in kwargs.items():
            # Ignore unknown fields
            if key not in valid_fields:
                continue

            setattr(self, key, value)
