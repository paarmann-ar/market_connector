import json
from dataclasses import asdict, dataclass, field
from typing import Any, Optional

from apis.zalando_lounge_api.models.zalando_lounge_media_model import (
    ZalandoLoungeMediaModel,
)
from apis.zalando_lounge_api.models.zalando_lounge_simple_model import (
    ZalandoLoungeSimpleModel,
)

# --
# ...
# --


@dataclass
class ZalandoLoungeProductModel:
    #  --
    #  ...
    #  --
    energy_efficiency_class: Optional[str] = None

    model_identifier: Optional[str] = None

    brand: Optional[str] = None
    brandCode: Optional[str] = None

    categoryId: Optional[int] = None
    campaignIdentifier: Optional[str] = None

    modelSku: Optional[str] = None
    sku: Optional[str] = None

    #  --------------------------------------------------
    #  Names / category
    #  --------------------------------------------------

    nameCategoryTag: Optional[str] = None
    nameColor: Optional[str] = None
    nameShop: Optional[str] = None
    subtitle: Optional[str] = None

    silhouette: Optional[str] = None

    #  --------------------------------------------------
    #  Product information
    #  --------------------------------------------------

    gender: list[str] = field(default_factory=list)

    targetGroups: list[str] = field(default_factory=list)

    attributes: dict[str, Any] = field(default_factory=dict)

    description: list[dict[str, Any]] = field(default_factory=list)

    product_highlights: list[str] = field(default_factory=list)

    #  --------------------------------------------------
    #  Images / Media
    #  --------------------------------------------------

    images: list[str] = field(default_factory=list)

    media: list[ZalandoLoungeMediaModel] = field(default_factory=list)

    #  --------------------------------------------------
    #  Price
    #  --------------------------------------------------

    price: Optional[int] = None
    specialPrice: Optional[int] = None
    savings: Optional[int] = None

    similarPrices: Optional[bool] = None

    #  --------------------------------------------------
    #  Stock
    #  --------------------------------------------------

    stockStatus: Optional[str] = None

    #  --------------------------------------------------
    #  Variations
    #  --------------------------------------------------

    simples: list[ZalandoLoungeSimpleModel] = field(default_factory=list)

    #  --------------------------------------------------
    #  Delivery / Shipping
    #  --------------------------------------------------

    delivery_promise: Optional[dict[str, Any]] = None

    shipping_fee: Optional[dict[str, Any]] = None

    #  --------------------------------------------------
    #  Manufacturer
    #  --------------------------------------------------

    manufacturer_details: Optional[dict[str, Any]] = None

    #  --------------------------------------------------
    #  Campaign / category
    #  --------------------------------------------------

    urlPath: dict[str, str] = field(default_factory=dict)

    globalCategoryIds: list[str] = field(default_factory=list)

    filters: list[dict[str, Any]] = field(default_factory=list)

    #  --------------------------------------------------
    #  Other
    #  --------------------------------------------------

    season: Optional[str] = None

    sustainable: bool = False

    sustainabilityCertificate: list[Any] = field(default_factory=list)

    hasSimilar: Optional[bool] = None
    hasTestMedia: Optional[bool] = None
    hasManufacturingAttributes: Optional[bool] = None

    plusEarlyAccess: Optional[bool] = None

    sizechartUrl: Optional[str] = None

    colorFamilyKey: Optional[int] = None

    taxCode: Optional[int] = None

    #  --------------------------------------------------
    #  ...
    #  --------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    #  --------------------------------------------------
    #  ...
    #  --------------------------------------------------

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            ensure_ascii=False,
        )

    #  --------------------------------------------------
    #  ...
    #  --------------------------------------------------

    def get_all_attributes(self) -> dict[str, Any]:
        return self.to_dict()

    #  --------------------------------------------------
    #  API -> Model
    #  --------------------------------------------------

    @classmethod
    def from_api(
        cls,
        data: dict[str, Any],
    ) -> "ZalandoLoungeProductModel":

        media = [ZalandoLoungeMediaModel.from_api(item) for item in data.get("media", []) if isinstance(item, dict)]

        simples = [ZalandoLoungeSimpleModel.from_api(item) for item in data.get("simples", []) if isinstance(item, dict)]

        return cls(
            #  --------------------------------------------------
            #  Basic
            #  --------------------------------------------------
            energy_efficiency_class=data.get("energy_efficiency_class"),
            model_identifier=data.get("model_identifier"),
            brand=data.get("brand"),
            brandCode=data.get("brandCode"),
            categoryId=data.get("categoryId"),
            campaignIdentifier=data.get("campaignIdentifier"),
            modelSku=data.get("modelSku"),
            sku=data.get("sku"),
            #  --------------------------------------------------
            #  Names
            #  --------------------------------------------------
            nameCategoryTag=data.get("nameCategoryTag"),
            nameColor=data.get("nameColor"),
            nameShop=data.get("nameShop"),
            subtitle=data.get("subtitle"),
            silhouette=data.get("silhouette"),
            #  --------------------------------------------------
            #  Product information
            #  --------------------------------------------------
            gender=data.get(
                "gender",
                [],
            ),
            targetGroups=data.get(
                "targetGroups",
                [],
            ),
            attributes=data.get(
                "attributes",
                {},
            ),
            description=data.get(
                "description",
                [],
            ),
            product_highlights=data.get(
                "product_highlights",
                [],
            ),
            #  --------------------------------------------------
            #  Images
            #  --------------------------------------------------
            images=data.get(
                "images",
                [],
            ),
            media=media,
            #  --------------------------------------------------
            #  Price
            #  --------------------------------------------------
            price=data.get("price"),
            specialPrice=data.get("specialPrice"),
            savings=data.get("savings"),
            similarPrices=data.get("similarPrices"),
            #  --------------------------------------------------
            #  Stock
            #  --------------------------------------------------
            stockStatus=data.get("stockStatus"),
            #  --------------------------------------------------
            #  Variations
            #  --------------------------------------------------
            simples=simples,
            #  --------------------------------------------------
            #  Delivery
            #  --------------------------------------------------
            delivery_promise=data.get("delivery_promise"),
            shipping_fee=data.get("shipping_fee"),
            #  --------------------------------------------------
            #  Manufacturer
            #  --------------------------------------------------
            manufacturer_details=data.get("manufacturer_details"),
            #  --------------------------------------------------
            #  Campaign / category
            #  --------------------------------------------------
            urlPath=data.get(
                "urlPath",
                {},
            ),
            globalCategoryIds=data.get(
                "globalCategoryIds",
                [],
            ),
            filters=data.get(
                "filters",
                [],
            ),
            #  --------------------------------------------------
            #  Other
            #  --------------------------------------------------
            season=data.get("season"),
            sustainable=data.get(
                "sustainable",
                False,
            ),
            sustainabilityCertificate=data.get(
                "sustainabilityCertificate",
                [],
            ),
            hasSimilar=data.get("hasSimilar"),
            hasTestMedia=data.get("hasTestMedia"),
            hasManufacturingAttributes=data.get("hasManufacturingAttributes"),
            plusEarlyAccess=data.get("plusEarlyAccess"),
            sizechartUrl=data.get("sizechartUrl"),
            colorFamilyKey=data.get("colorFamilyKey"),
            taxCode=data.get("taxCode"),
        )
