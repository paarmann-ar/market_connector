from dataclasses import dataclass, field

from apis.woocommerce_api.models.woocommerce_brand_model import WoocommerceBrandModel
from apis.woocommerce_api.models.woocommerce_category_model import (
    WoocommerceCategoryModel,
)
from apis.woocommerce_api.models.woocommerce_product_model import (
    WoocommerceProductModel,
)
from apis.woocommerce_api.models.woocommerce_tag_model import WoocommerceTagModel
from apis.wordpress_api.models.wordpress_media_model import WordpressMediaModel
from pydantic import BaseModel

# --
# ...
# --


class WoocommerceSessionModel(BaseModel):
    products: list[WoocommerceProductModel] = field(default_factory=list)
    categories: list[WoocommerceCategoryModel] = field(default_factory=list)
    tags: list[WoocommerceTagModel] = field(default_factory=list)
    brands: list[WoocommerceBrandModel] = field(default_factory=list)
    media: list[WordpressMediaModel] = field(default_factory=list)

    # --
    # ...
    # --

    def add_product(self, product: WoocommerceProductModel):
        self.products.append(product)

    # --
    # ...
    # --

    def add_category(self, category: WoocommerceCategoryModel):
        self.categories.append(category)

    # --
    # ...
    # --

    def add_tag(self, tag: WoocommerceTagModel):
        self.tags.append(tag)

    # --
    # ...
    # --

    def add_brand(self, brand: WoocommerceBrandModel):
        self.brands.append(brand)

    # --
    # ...
    # --

    def add_media(self, media: WordpressMediaModel):
        self.media.append(media)
