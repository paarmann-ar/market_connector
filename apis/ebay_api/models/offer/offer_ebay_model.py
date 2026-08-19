from dataclasses import asdict, dataclass, fields
from typing import Any, Optional
import json
# --
# ...
# --


@dataclass
class OfferEbayModel:
    sku: Optional[str] = None
    marketplaceId: Optional[str] = None
    format: Optional[str] = "FIXED_PRICE"
    categoryId: Optional[str] = None
    merchantLocationKey: Optional[str] = None
    availableQuantity: Optional[int] = 1
    listingDescription: Optional[str] = None
    listingDuration: Optional[str] = "GTC"
    pricingSummary: Optional[dict[str, Any]] = None
    listingPolicies: Optional[dict[str, Any]] = None
    lotSize: Optional[int] = None
    inventory_location_model: Optional[Any] = None

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

    # --
    # ...
    # --

    def to_dict(self) -> dict[str, Any]:

        data = asdict(self)

        # Remove None values
        return {key: value for key, value in data.items() if value is not None}

    # --
    # ...
    # --

    def to_json(self) -> str:

        return json.dumps(
            self.to_dict(),
            ensure_ascii=False,
        )
