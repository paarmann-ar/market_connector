import json
from dataclasses import asdict, dataclass, fields
from typing import Optional, Any
from apis.ebay_api.models.image_ebay_model import ImageEbayModel
from apis.ebay_api.models.seller_ebay_model import SellerEbayModel

# --
# ...
# --

@dataclass
class ProductEbayModel:
    itemId: Optional[str] = None
    sellerItemRevision: Optional[str] = None
    title: Optional[str] = None
    shortDescription: Optional[str] = None
    price: Optional[str] = None
    currency: Optional[str] = None
    categoryPath: Optional[str] = None
    categoryIdPath: Optional[str] = None
    condition: Optional[str] = None
    conditionId: Optional[str] = None
    itemLocation: Optional[str] = None
    stateOrProvince: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None
    image: Optional[ImageEbayModel] = None
    brand: Optional[str] = None
    itemCreationDate: Optional[str] = None
    seller: Optional[SellerEbayModel] = None
    gtin: Optional[str] = None
    mpn: Optional[str] = None
    estimatedAvailabilities: Optional[Any]=None
    shippingOptions: Optional[Any]=None
    shipToLocations: Optional[Any]=None
    returnTerms: Optional[Any]=None
    taxes: Optional[Any]=None
    localizedAspects: Optional[Any]=None
    topRatedBuyingExperience: Optional[str] = None
    buyingOptions: Optional[Any]=None
    itemWebUrl: Optional[str] = None
    description: Optional[str] = None
    paymentMethods: Optional[Any]=None
    immediatePay: Optional[str] = None
    enabledForGuestCheckout: Optional[str] = None
    eligibleForInlineCheckout: Optional[str] = None
    lotSize: Optional[str] = None
    legacyItemId: Optional[str] = None
    priorityListing: Optional[str] = None
    adultOnly: Optional[str] = None
    categoryId: Optional[str] = None
    listingMarketplaceId: Optional[str] = None
    price_anpassen: Optional[int] = 1.60
    additionalImages : Optional[Any] = None

    # --
    # ...
    # --

    def __init__(self, **kwargs):
        valid_fields = {f.name for f in fields(self)}

        for key, value in kwargs.items():
            if key in valid_fields:
                setattr(self, key, value)

    # --
    # ...
    # --

    def to_json(self):
        return json.dumps(asdict(self), ensure_ascii=False)

    # --
    # ...
    # --

    def to_dict(self):
        data = asdict(self)
        return data

    # --
    # ...
    # --

    def generate_filter(self):
        self.filter = f"conditions:{self.conditions},deliveryCountry:{self.deliveryCountry},{self.filter}"

    # --
    # ...
    # --

    def get_all_attributes(self):
        return asdict(self)
