from typing import Optional
from apis.matterhorn_moda_api.models.product_matterhorn_moda_model import ProductMatterhornModaModel
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
from apis.matterhorn_moda_api.models.search_in_matterhorn_moda_model import SearchInMatterhornModaModel
from market_services.meta_data_services.meta_data_services import MetaDataServices
from market_services.adapters.models.validate_final_model import ValidateFinalModel
from market_services.adapters.matterhorn.matterhorn_moda_product_model_to_woocommerce_product_input_metadata_model import (
    MatterhornModaProductModelToWoocommerceProductInputMetadataModel,
)
from market_services.adapters.matterhorn.matterhorn_moda_assembel_final import assemble_final
# --
# ...
# --


class MatterhornModaProductModelToWoocommerceProductModelAdaptor:
    def adapter(
        self, product_matterhorn_moda_model: ProductMatterhornModaModel, search_in_matterhorn_moda_model: SearchInMatterhornModaModel
    ) -> WoocommerceProductModel:

        meta_data_services = MetaDataServices()
        product_output_metadata_model = meta_data_services.create_metadata(
            product_input_metadata_model=MatterhornModaProductModelToWoocommerceProductInputMetadataModel().adapter(
                product_matterhorn_moda_model=product_matterhorn_moda_model, prompt_filename="miviva_matterhorn_moda_product",is_remove_html=search_in_matterhorn_moda_model.is_remove_description_html
            ),assemble_final=assemble_final, product_model=product_matterhorn_moda_model
        )

        woocommerce_tags_model = []
        for tag in product_output_metadata_model.product_tags:
            woocommerce_tag_model = WoocommerceTagModel(name=tag)
            woocommerce_tags_model.append(woocommerce_tag_model)

        woocommerce_images_model: list = []
        image_alt = product_output_metadata_model.image_seo_model.get("image_alt")

        for image_url in product_matterhorn_moda_model.images:
            woocommerce_images_model.append(WoocommerceImageModel.from_api({"src": image_url, "alt": image_alt}))

        return WoocommerceProductModel(
            name=product_output_metadata_model.title or "",
            description=product_output_metadata_model.description or "",
            short_description=product_output_metadata_model.short_description or "",
            image_description=product_output_metadata_model.image_description or "",
            sku=f"mm_{product_matterhorn_moda_model.id}" or "",
            on_sale=True,
            manage_stock=True,
            categories=self._get_categories(product_matterhorn_moda_model),
            brands=self._get_brands(product_matterhorn_moda_model),
            tags=woocommerce_tags_model,
            images=self._get_images(product_matterhorn_moda_model),
            stock_status=self._get_stock_status(product_matterhorn_moda_model),
        )

    # ------------------------------------------------------------------
    # Category
    # ------------------------------------------------------------------

    def _get_categories(
        self,
        product_matterhorn_moda_model: ProductMatterhornModaModel,
    ) -> list[WoocommerceCategoryModel]:

        category_name = product_matterhorn_moda_model.category_name
        category_path = product_matterhorn_moda_model.category_path

        return [WoocommerceCategoryModel(name=category_name, slug=self._slugify(category_name), path=category_path)]

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

        for index, image_url in enumerate(product_matterhorn_moda_model.images):
            if not image_url:
                continue

            images.append(
                WoocommerceImageModel(
                    src=image_url,
                    name=product_matterhorn_moda_model.name,
                    alt=product_matterhorn_moda_model.name,
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

        return value.strip().lower().replace(" ", "-")
