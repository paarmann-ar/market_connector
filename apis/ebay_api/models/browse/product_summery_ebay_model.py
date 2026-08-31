import json
from dataclasses import asdict, dataclass, fields
from typing import Any, Optional

# --
# ...
# --


@dataclass
class ProductSummeryEbayModel:
    itemId: Optional[str] = None
    title: Optional[str] = None
    leafCategoryIds: Optional[Any] = None
    categories: Optional[Any] = None
    image: Optional[Any] = None
    price: Optional[Any] = None
    itemHref: Optional[str] = None
    seller: Optional[Any] = None
    marketingPrice: Optional[Any] = None
    condition: Optional[str] = None
    conditionId: Optional[str] = None
    thumbnailImages: Optional[Any] = None
    shippingOptions: Optional[Any] = None
    buyingOptions: Optional[Any] = None
    itemWebUrl: Optional[str] = None
    itemLocation: Optional[Any] = None
    additionalImages: Optional[Any] = None
    adultOnly: Optional[str] = None
    legacyItemId: Optional[str] = None
    availableCoupons: Optional[str] = None
    itemOriginDate: Optional[str] = None
    itemCreationDate: Optional[str] = None
    topRatedBuyingExperience: Optional[str] = None
    priorityListing: Optional[str] = None
    listingMarketplaceId: Optional[str] = None

    #  --
    #  ...
    #  --

    def __init__(self, **kwargs):
        valid_fields = {f.name for f in fields(self)}

        for key, value in kwargs.items():
            if key in valid_fields:
                setattr(self, key, value)

    #  --
    #  ...
    #  --

    def to_json(self):
        return json.dumps(asdict(self), ensure_ascii=False)

    #  --
    #  ...
    #  --

    def to_dict(self):
        data = asdict(self)
        return data

    #  --
    #  ...
    #  --

    def generate_filter(self):
        self.filter = f"conditions:{self.conditions},deliveryCountry:{self.deliveryCountry},{self.filter}"

    #  --
    #  ...
    #  --

    def get_all_attributes(self):
        return asdict(self)
