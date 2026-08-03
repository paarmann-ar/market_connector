import json
from dataclasses import asdict, dataclass, field
from typing import Optional

from apis.woocommerce_api.models.woocommerce_brand_model import WoocommerceBrandModel
from apis.woocommerce_api.models.woocommerce_category_model import (
    WoocommerceCategoryModel,
)
from apis.woocommerce_api.models.woocommerce_image_model import WoocommerceImageModel
from apis.woocommerce_api.models.woocommerce_tag_model import WoocommerceTagModel

# --
# ...
# --


@dataclass
class WoocommerceProductModel:
    id: Optional[int] = None
    name: Optional[str] = ""
    slug: Optional[str] = ""
    permalink: Optional[str] = ""
    catalog_visibility: Optional[str] = "visible"
    description: Optional[str] = ""
    short_description: Optional[str] = ""
    sku: Optional[str] = ""
    price: Optional[str] = ""
    regular_price: Optional[str] = ""
    sale_price: Optional[str] = ""
    on_sale: Optional[bool] = False
    tax_status: Optional[str] = "taxable"
    tax_class: Optional[str] = ""
    manage_stock: Optional[bool] = False
    shipping_required: Optional[bool] = True
    shipping_taxable: Optional[bool] = True
    shipping_class: Optional[str] = ""
    shipping_class_id: Optional[int] = 0
    categories: list[WoocommerceCategoryModel] = field(default_factory=list)
    brands: list[WoocommerceBrandModel] = field(default_factory=list)
    tags: list[WoocommerceTagModel] = field(default_factory=list)
    images: list[WoocommerceImageModel] = field(default_factory=list)
    attributes: list = field(default_factory=list)
    default_attributes: list[str] = field(default_factory=list)
    stock_status: Optional[str] = "instock"

    # --
    # ...
    # --

    def to_json(self):
        return json.dumps(asdict(self), ensure_ascii=False)

    # --
    # ...
    # --

    def to_dict(self):
        return asdict(self)

    # --
    # ...
    # --

    @classmethod
    def from_api(cls, data):
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
        )
