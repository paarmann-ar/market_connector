from itertools import product
from apis.woocommerce_api.config.woocommerce_api_config import WoocommerceApiConfig
from apis.woocommerce_api.core.base_woocommerce_api import BaseWoocommerceApi
from apis.woocommerce_api.models.search_in_woocommerce_model import SearchInWoocommerceModel
from apis.woocommerce_api.models.woocommerce_category_model import WoocommerceCategoryModel
from apis.woocommerce_api.models.woocommerce_product_model import WoocommerceProductModel
from apis.woocommerce_api.models.woocommerce_attribute_model import WoocommerceAttributeModel
from apis.woocommerce_api.models.woocommerce_attribute_model import WoocommerceProductAttributeModel
from apis.woocommerce_api.models.woocommerce_attribute_model import WoocommerceAttributeTermModel
from apis.woocommerce_api.models.woocommerce_variation_attribute_model import WoocommerceVariationModel
from apis.woocommerce_api.models.woocommerce_variation_attribute_model import WoocommerceVariationAttributeModel
from apis.woocommerce_api.services.woocommerce_brand import WoocommerceBrand
from apis.woocommerce_api.services.woocommerce_category import WoocommerceCategory
from apis.woocommerce_api.services.woocommerce_image import WoocommerceImage
from apis.woocommerce_api.services.woocommerce_product import WoocommerceProduct
from apis.woocommerce_api.services.woocommerce_rollback import WoocommerceRollback
from apis.woocommerce_api.services.woocommerce_tag import WoocommerceTag
from apis.woocommerce_api.services.woocommerce_attribute import WoocommerceAttribute
from toolboxs.dict_utils import remove_none


# --
# ...
# --


class WoocommerceApi(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:

        super().__init__(**kwargs)

        self.base_url = self.config_dictionary.get("base_url")
        self.wp_media_url = self.config_dictionary.get("wp_media_url")
        self.consumer_key = self.config_dictionary.get("consumer_key")
        self.consumer_secret = self.config_dictionary.get("consumer_secret")
        self.wp_user = self.config_dictionary.get("wp_user")
        self.wp_password = self.config_dictionary.get("wp_password")
        self.products_url = self.config_dictionary.get("products_url")

        self.woocommerce_product = WoocommerceProduct()
        self.woocommerce_rollback = WoocommerceRollback()

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return WoocommerceApiConfig().get_dictionary()

    # --
    # ...
    # --

    def upload_product_model_to_woocommerce(
        self, woocommerce_product_models: list[WoocommerceProductModel], target_woocommerce_category_name: str
    ) -> bool:

        for woocommerce_product_model in woocommerce_product_models:
            if target_woocommerce_category_name:
                target_category = WoocommerceCategoryModel(name=target_woocommerce_category_name)

                woocommerce_product_model.categories = [target_category]

            woocommerce_product_model = self.resolve_or_upload(woocommerce_product_model)

            if not woocommerce_product_model:
                continue

            self.waiting(1000)

            # ------------------------------------------
            # VARIATIONS
            # ------------------------------------------

            if woocommerce_product_model.type == "variable":
                self.create_product_variations(woocommerce_product_model)

            self.waiting(1000)

        return True

    # --
    # ...
    # --

    def resolve_or_upload(self, woocommerce_product_model: WoocommerceProductModel) -> WoocommerceProductModel:

        try:
            # ------------------------------------------
            # CHECK PRODUCT
            # ------------------------------------------

            product = self.woocommerce_product.get_product_by_name(woocommerce_product_model.name)

            if product:
                return product

            # ------------------------------------------
            # RESULT MODELS
            # ------------------------------------------

            woocommerce_categories_model = []
            woocommerce_brands_model = []
            woocommerce_tags_model = []
            woocommerce_images_model = []
            woocommerce_product_attribute_models = []

            # ------------------------------------------
            # IMAGES
            # ------------------------------------------

            woocommerce_image = WoocommerceImage()

            for image in woocommerce_product_model.images:
                uploaded_image = woocommerce_image.resolve_or_upload(image)

                if uploaded_image:
                    woocommerce_images_model.append(uploaded_image)

            # ------------------------------------------
            # CATEGORIES
            # ------------------------------------------

            woocommerce_category = WoocommerceCategory()
            for category in woocommerce_product_model.categories:
                try:
                    uploaded_category = woocommerce_category.resolve_or_upload(category)

                    if uploaded_category:
                        woocommerce_categories_model.append(uploaded_category)

                except Exception as exp:
                    self.error(f"Could not resolve category '{category.name}': {exp}")
                    continue

            # ------------------------------------------
            # BRANDS
            # ------------------------------------------

            woocommerce_brand = WoocommerceBrand()

            for brand in woocommerce_product_model.brands:
                if not brand.name:
                    brand.name = "NoBrand"

                uploaded_brand = woocommerce_brand.resolve_or_upload(brand)

                if uploaded_brand:
                    woocommerce_brands_model.append(uploaded_brand)

            # ------------------------------------------
            # TAGS
            # ------------------------------------------

            woocommerce_tag = WoocommerceTag()

            for tag in woocommerce_product_model.tags:
                uploaded_tag = woocommerce_tag.resolve_or_upload(tag)

                if uploaded_tag:
                    woocommerce_tags_model.append(uploaded_tag)

            # ------------------------------------------
            # ATTRIBUTES
            # ------------------------------------------

            woocommerce_attribute = WoocommerceAttribute()

            for product_attribute in woocommerce_product_model.attributes:
                # --------------------------------------
                # GLOBAL ATTRIBUTE
                # --------------------------------------

                attribute = woocommerce_attribute.resolve_or_upload(WoocommerceAttributeModel(name=product_attribute.name))

                if not attribute:
                    raise ValueError(f"Could not create attribute: {product_attribute.name}")

                if not attribute.id:
                    raise ValueError(f"Attribute has no ID: {product_attribute.name}")

                # --------------------------------------
                # TERMS
                # --------------------------------------

                resolved_options = []

                for option in product_attribute.options:
                    term = woocommerce_attribute.resolve_or_upload_term(
                        attribute_id=attribute.id,
                        term_model=(WoocommerceAttributeTermModel(name=option)),
                    )

                    if term:
                        resolved_options.append(term.name)

                    else:
                        resolved_options.append(option)

                # --------------------------------------
                # PRODUCT ATTRIBUTE
                # --------------------------------------

                woocommerce_product_attribute_models.append(
                    WoocommerceProductAttributeModel(
                        id=attribute.id,
                        name=attribute.name,
                        options=resolved_options,
                        visible=True,
                        variation=True,
                    )
                )

            # ------------------------------------------
            # VARIABLE PRODUCT
            # ------------------------------------------

            if woocommerce_product_attribute_models:
                woocommerce_product_model.type = "variable"

            # ------------------------------------------
            # ASSIGN RESOLVED DATA
            # ------------------------------------------

            woocommerce_product_model.images = woocommerce_images_model
            woocommerce_product_model.categories = woocommerce_categories_model
            woocommerce_product_model.brands = woocommerce_brands_model
            woocommerce_product_model.tags = woocommerce_tags_model
            woocommerce_product_model.attributes = woocommerce_product_attribute_models

            # ------------------------------------------
            # REMOVE NONE
            # ------------------------------------------

            woocommerce_product_model = remove_none(woocommerce_product_model)

            # ------------------------------------------
            # UPLOAD PRODUCT
            # ------------------------------------------

            woocommerce_product_model = self.woocommerce_product.upload_product(woocommerce_product_model=woocommerce_product_model)

            if not woocommerce_product_model:
                raise ValueError("Product upload failed")

            return woocommerce_product_model

        except Exception as exp:
            self.error(f"resolve_or_upload: {exp}")

            return None

    # --
    # ...
    # --

    def build_variation_rows(
        self,
        attributes: list[WoocommerceProductAttributeModel],
    ) -> list[dict[str, str]]:

        if not attributes:
            return []

        attribute_names = []

        attribute_options = []

        for attribute in attributes:
            if not attribute.id:
                continue

            if not attribute.options:
                continue

            attribute_names.append(attribute.name)

            attribute_options.append(attribute.options)

        if not attribute_names:
            return []

        rows = []

        for combination in product(*attribute_options):
            row = {}

            for name, option in zip(attribute_names, combination):
                row[name] = option

            rows.append(row)

        return rows

    # --
    # ...
    # --

    def create_product_variations(
        self,
        woocommerce_product_model: WoocommerceProductModel,
    ):

        if not woocommerce_product_model.id:
            raise ValueError("Product ID is required")

        if not woocommerce_product_model.attributes:
            return

        # ------------------------------------------
        # BUILD COMBINATIONS
        # ------------------------------------------

        variation_rows = self.build_variation_rows(woocommerce_product_model.attributes)

        # ------------------------------------------
        # CREATE VARIATIONS
        # ------------------------------------------

        sku_index = 1
        for row in variation_rows:
            variation_attributes = []

            for attribute in woocommerce_product_model.attributes:
                if not attribute.id:
                    continue

                option = row.get(attribute.name)

                if option is None:
                    continue

                variation_attributes.append(WoocommerceVariationAttributeModel(id=attribute.id, name=attribute.name, option=option))

            if not variation_attributes:
                continue

            for variant in woocommerce_product_model.variants:
                if variant.name == option:
                    stock_quantity = variant.stock
                    break

            variation_model = WoocommerceVariationModel(
                sku=f"{woocommerce_product_model.sku}-{sku_index}",
                attributes=variation_attributes,
                regular_price=(woocommerce_product_model.regular_price),
                sale_price=(woocommerce_product_model.sale_price),
                manage_stock=True,
                stock_quantity=stock_quantity,
                stock_status=self._get_stock_status(stock_quantity),
            )

            self.woocommerce_product.upload_variation(product_id=(woocommerce_product_model.id), variation_model=variation_model)

            sku_index += 1

    #  ------------------------------------------------------------------
    #  Stock
    #  ------------------------------------------------------------------

    def _get_stock_status(
        self,
        stock_quantity: int,
    ) -> str:

        if (stock_quantity or 0) > 0:
            return "instock"

        return "outofstock"

    # --
    # ...
    # --

    def fetch_from_woocommerce(self, search_in_woocommerce_model: SearchInWoocommerceModel) -> WoocommerceProductModel:

        woocommerce_product_models = self.woocommerce_product.get_product_by_search_in_woocommerce_model(
            search_in_woocommerce_model=(search_in_woocommerce_model)
        )

        return woocommerce_product_models
