from typing import Optional
from apis.matterhorn_moda_api .models.product_matterhorn_moda_model import ProductMatterhornModaModel
from apis.woocommerce_api.models.woocommerce_product_model import (
    WoocommerceProductModel,
)
from apis.woocommerce_api.models.woocommerce_category_model import (
    WoocommerceCategoryModel,
)
from apis.woocommerce_api.models.woocommerce_brand_model import (
    WoocommerceBrandModel,
)
from apis.woocommerce_api.models.woocommerce_image_model import (
    WoocommerceImageModel,
)
from apis.woocommerce_api.models.woocommerce_tag_model import (
    WoocommerceTagModel,
)

# --
# ...
# --


class MatterhornModaProductModelToWoocommerceProductModelAdaptor:
    def adapter(self, product_matterhorn_moda_model: ProductMatterhornModaModel) -> WoocommerceProductModel:
        return WoocommerceProductModel(
            name=product_matterhorn_moda_model.name_without_number or "",
            description=product_matterhorn_moda_model.description or "",
            short_description=product_matterhorn_moda_model.description or "",
            image_description=product_matterhorn_moda_model.name or "",
            sku=f"mm_{product_matterhorn_moda_model.id}" or "",

            price=self._get_price(product_matterhorn_moda_model),
            regular_price=self._get_price(product_matterhorn_moda_model),

            on_sale=True,

            manage_stock=True,

            categories=self._get_categories(
                product_matterhorn_moda_model
            ),

            brands=self._get_brands(
                product_matterhorn_moda_model
            ),

            tags=[],

            images=self._get_images(
                product_matterhorn_moda_model
            ),

            stock_status=self._get_stock_status(
                product_matterhorn_moda_model
            ),
        )

    # ------------------------------------------------------------------
    # Price
    # ------------------------------------------------------------------

    def _get_price(
        self,
        product_matterhorn_moda_model: ProductMatterhornModaModel,
    ) -> str:

        if not product_matterhorn_moda_model.prices:
            return ""

        if product_matterhorn_moda_model.prices.EUR is None:
            return ""

        return str(product_matterhorn_moda_model.prices.EUR * 1.4)

    # ------------------------------------------------------------------
    # Category
    # ------------------------------------------------------------------

    def _get_categories(
        self,
        product_matterhorn_moda_model: ProductMatterhornModaModel,
    ) -> list[WoocommerceCategoryModel]:

        category_name = product_matterhorn_moda_model.category_name
        category_path = product_matterhorn_moda_model.category_path


        return [
            WoocommerceCategoryModel(
                name=category_name,
                slug=self._slugify(category_name),
                description=category_path,
            )
        ]

    # ------------------------------------------------------------------
    # Brand
    # ------------------------------------------------------------------

    def _get_brands(
        self,
        product_matterhorn_moda_model: ProductMatterhornModaModel,
    ) -> list[WoocommerceBrandModel]:

        brand_name = product_matterhorn_moda_model.brand

        return [
            WoocommerceBrandModel(
                name=brand_name or "No Brand",
                slug=self._slugify(brand_name),
                description=None,
            )
        ]

    # ------------------------------------------------------------------
    # Images
    # ------------------------------------------------------------------

    def _get_images(
        self,
        product_matterhorn_moda_model: ProductMatterhornModaModel,
    ) -> list[WoocommerceImageModel]:

        if not product_matterhorn_moda_model.images:
            return []

        images = []

        for index, image_url in enumerate(
            product_matterhorn_moda_model.images
        ):
            if not image_url:
                continue

            images.append(
                WoocommerceImageModel(
                    src=image_url,
                    name=product_matterhorn_moda_model.name,
                    alt=product_matterhorn_moda_model.name,
                    is_main_image=index == 0,
                )
            )

        return images

    # ------------------------------------------------------------------
    # Stock
    # ------------------------------------------------------------------

    def _get_stock_status(
        self,
        product_matterhorn_moda_model: ProductMatterhornModaModel,
    ) -> str:

        if (product_matterhorn_moda_model.stock_total or 0) > 0:
            return "instock"

        return "outofstock"

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _to_int(value: Optional[str | int]) -> Optional[int]:

        if value is None or value == "":
            return None

        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _slugify(value: Optional[str]) -> Optional[str]:

        if not value:
            return None

        return (
            value.strip()
            .lower()
            .replace(" ", "-")
        )