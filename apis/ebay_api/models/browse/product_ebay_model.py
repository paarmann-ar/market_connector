import json
from dataclasses import asdict, dataclass, fields
from typing import Any, Optional

from apis.ebay_api.models.browse.image_ebay_model import ImageEbayModel
from apis.ebay_api.models.browse.seller_ebay_model import SellerEbayModel
from toolboxs.html import Html

# --
# ...
# --


@dataclass
class ProductEbayModel:
    itemId: Optional[str] = None
    sellerItemRevision: Optional[str] = None

    sku: Optional[str] = None
    title: Optional[str] = None
    shortDescription: Optional[str] = None
    description: Optional[str] = None

    price: Optional[str] = None
    currency: Optional[str] = None

    categoryPath: Optional[str] = None
    categoryIdPath: Optional[str] = None
    categoryId: Optional[str] = None

    condition: Optional[str] = None
    conditionId: Optional[str] = None
    conditionDescription: Optional[str] = None

    itemLocation: Optional[str] = None
    stateOrProvince: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None

    image: Optional[ImageEbayModel] = None
    additionalImages: Optional[list[ImageEbayModel]] = None

    brand: Optional[str] = None
    mpn: Optional[str] = None
    gtin: Optional[str] = None

    itemCreationDate: Optional[str] = None

    seller: Optional[SellerEbayModel] = None

    estimatedAvailabilities: Optional[Any] = None
    shippingOptions: Optional[Any] = None
    shipToLocations: Optional[Any] = None
    returnTerms: Optional[Any] = None
    taxes: Optional[Any] = None

    localizedAspects: Optional[dict[str, list[str]]] = None

    topRatedBuyingExperience: Optional[bool] = None
    buyingOptions: Optional[list[str]] = None

    itemWebUrl: Optional[str] = None

    paymentMethods: Optional[Any] = None
    immediatePay: Optional[bool] = None

    enabledForGuestCheckout: Optional[bool] = None
    eligibleForInlineCheckout: Optional[bool] = None

    lotSize: Optional[int] = None
    legacyItemId: Optional[str] = None

    priorityListing: Optional[bool] = None
    adultOnly: Optional[bool] = None

    listingMarketplaceId: Optional[str] = None

    price_anpassen: Optional[float] = 1.60

    # eBay item specifics
    aspects: Optional[dict[str, list[str]]] = None
    sellerAccountType: Optional[str] = None

    # --
    # ...
    # --

    def __init__(self, **kwargs):

        valid_fields = {field.name for field in fields(self)}

        for key, value in kwargs.items():
            # Ignore unknown fields
            if key not in valid_fields:
                continue

            if key == "description" or key == "shortDescription":
                value = Html.remove_html_tags(value, 3990)

            if key == "image":
                if isinstance(value, dict):
                    value = ImageEbayModel(**value)

            elif key == "additionalImages":
                if isinstance(value, list):
                    value = [ImageEbayModel(**image) if isinstance(image, dict) else image for image in value]

            elif key == "seller":
                if isinstance(value, dict):
                    value = SellerEbayModel(**value)

            setattr(self, key, value)

    # --
    # ...
    # --

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    # --
    # ...
    # --

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            ensure_ascii=False,
        )

    # --
    # ...
    # --

    def get_all_attributes(self) -> dict[str, Any]:
        return self.to_dict()

    # --
    # ...
    # --

    @staticmethod
    def parse_images(value) -> list[ImageEbayModel]:

        if not value:
            return []

        return [ImageEbayModel(**image) if isinstance(image, dict) else image for image in value if image]
