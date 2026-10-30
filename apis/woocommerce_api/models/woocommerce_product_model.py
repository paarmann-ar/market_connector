from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from apis.seo_api.models.rank_math_model import RankMathModel
from apis.woocommerce_api.models.woocommerce_brand_model import WoocommerceBrandModel
from apis.woocommerce_api.models.woocommerce_google_product_model import WoocommerceGoogleProductModel

from apis.woocommerce_api.models.woocommerce_category_model import (
    WoocommerceCategoryModel,
)
from apis.woocommerce_api.models.woocommerce_image_model import WoocommerceImageModel
from apis.woocommerce_api.models.woocommerce_tag_model import WoocommerceTagModel
from apis.woocommerce_api.models.woocommerce_attribute_model import WoocommerceAttributeModel
from apis.woocommerce_api.models.woocommerce_attribute_model import WoocommerceAttributeTermModel, WoocommerceProductAttributeModel
from enum import Enum

# --
# ...
# --
class Condition(str, Enum):
    NEW = "NEW"
    AS_NEW = "AS_NEW"
    REFURBISHED = "REFURBISHED"
    USED = "USED"


class ConditionValue(str, Enum):
    EXCELLENT = "EXCELLENT"
    VERY_GOOD = "VERY_GOOD"
    GOOD = "GOOD"
    ACCEPTABLE = "ACCEPTABLE"


class WoocommerceProductModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: Optional[int] = None
    name: Optional[str] = ""
    slug: Optional[str] = ""
    permalink: Optional[str] = ""
    catalog_visibility: Optional[str] = "visible"
    status: Optional[str] = "publish"
    description: Optional[str] = ""
    short_description: Optional[str] = ""
    image_description: Optional[str] = ""
    sku: Optional[str] = ""
    price: Optional[str] = ""
    regular_price: Optional[str] = ""
    sale_price: Optional[str] = ""
    on_sale: Optional[bool] = True
    tax_status: Optional[str] = "taxable"
    tax_class: Optional[str] = ""
    manage_stock: Optional[bool] = True
    stock_quantity: Optional[int] = 0
    stock_status: Optional[str] = "instock"
    shipping_required: Optional[bool] = True
    shipping_taxable: Optional[bool] = True
    shipping_class: Optional[str] = ""
    shipping_class_id: Optional[int] = 0

    categories: list[WoocommerceCategoryModel] = Field(default_factory=list)

    brands: list[WoocommerceBrandModel] = Field(default_factory=list)
    tags: list[WoocommerceTagModel] = Field(default_factory=list)
    images: list[WoocommerceImageModel] = Field(default_factory=list)
    image_description: Optional[str] = ""
    default_attributes: list[str] = Field(default_factory=list)

    condition: Condition = Condition.NEW
    condition_value: ConditionValue = ConditionValue.EXCELLENT
    meta_data: list[dict] = Field(default_factory=list)

    attributes: list[WoocommerceProductAttributeModel] = Field(default_factory=list)
    variants: list[object] = (None,)
    type: Optional[str] = "simple"

    #  --
    #  ...
    #  --

    def to_dict(self):
        data = self.model_dump(
            exclude_none=True,
            mode="json",
        )

        data["meta_data"] = [
            *data.get("meta_data", []),
            {
                "key": "condition",
                "value": self.condition.value,
            },
            {
                "key": "condition_value",
                "value": self.condition_value.value,
            },
        ]

        return data

    #  --
    #  ...
    #  --

    def to_json(self):
        return self.model_dump_json()

    #  --
    #  ...
    #  --

    @classmethod
    def from_api(cls, data):
        meta_data = data.get("meta_data", [])

        condition = Condition.NEW
        condition_value = ConditionValue.EXCELLENT

        for meta in meta_data:
            if meta.get("key") == "condition":
                try:
                    condition = Condition(meta.get("value"))
                except ValueError:
                    condition = Condition.NEW

            elif meta.get("key") == "condition_value":
                try:
                    condition_value = ConditionValue(meta.get("value"))
                except ValueError:
                    condition_value = ConditionValue.EXCELLENT

        return cls(
            id=data["id"],
            name=data["name"],
            slug=data["slug"],
            description=data["description"],
            permalink=data["permalink"],
            catalog_visibility=data["catalog_visibility"],
            short_description=data["short_description"],
            sku=data["sku"],
            price=data["price"],
            regular_price=data["regular_price"],
            sale_price=data["sale_price"],
            on_sale=data["on_sale"],
            tax_status=data["tax_status"],
            tax_class=data["tax_class"],
            manage_stock=data["manage_stock"],
            shipping_required=data["shipping_required"],
            shipping_taxable=data["shipping_taxable"],
            shipping_class=data["shipping_class"],
            shipping_class_id=data["shipping_class_id"],
            categories=data["categories"],
            brands=data["brands"],
            tags=data["tags"],
            images=data["images"],
            attributes=data["attributes"],
            default_attributes=data["default_attributes"],
            stock_status=data["stock_status"],
            type=data["type"],

            condition=condition,
            condition_value=condition_value,
            meta_data=meta_data,
        )
