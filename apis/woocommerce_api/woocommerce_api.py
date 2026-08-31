from apis.woocommerce_api.config.woocommerce_api_config import WoocommerceApiConfig
from apis.woocommerce_api.core.base_woocommerce_api import BaseWoocommerceApi
from apis.woocommerce_api.models.search_in_woocommerce_model import SearchInWoocommerceModel
from apis.woocommerce_api.models.woocommerce_brand_model import WoocommerceBrandModel
from apis.woocommerce_api.models.woocommerce_category_model import (
    WoocommerceCategoryModel,
)
from apis.woocommerce_api.models.woocommerce_image_model import WoocommerceImageModel
from apis.woocommerce_api.models.woocommerce_product_model import WoocommerceProductModel
from apis.woocommerce_api.models.woocommerce_session_model import WoocommerceSessionModel
from apis.woocommerce_api.models.woocommerce_tag_model import WoocommerceTagModel
from apis.woocommerce_api.services.woocommerce_brand import WoocommerceBrand
from apis.woocommerce_api.services.woocommerce_category import WoocommerceCategory
from apis.woocommerce_api.services.woocommerce_image import WoocommerceImage
from apis.woocommerce_api.services.woocommerce_product import WoocommerceProduct
from apis.woocommerce_api.services.woocommerce_rollback import WoocommerceRollback
from apis.woocommerce_api.services.woocommerce_tag import WoocommerceTag
from apis.woocommerce_api.services.woocommerce_attribute import WoocommerceAttribute
from apis.woocommerce_api.models.woocommerce_attribute_model import WoocommerceAttributeModel
from apis.woocommerce_api.models.woocommerce_attribute_model import WoocommerceProductAttributeModel
from apis.woocommerce_api.models.woocommerce_attribute_model import WoocommerceAttributeTermModel
from apis.woocommerce_api.models.woocommerce_variation_attribute_model import WoocommerceVariationModel
from apis.woocommerce_api.models.woocommerce_variation_attribute_model import WoocommerceVariationAttributeModel

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

        self.woocommerce_session_model = WoocommerceSessionModel()
        self.woocommerce_rollback = WoocommerceRollback()

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    #  --
    #  ...
    #  --

    @classmethod
    def get_config_dictionary(cls):
        return WoocommerceApiConfig().get_dictionary()

    #  --
    #  ...
    #  --

    def upload_product_model_to_woocommerce(
        self, woocommerce_product_models: list[WoocommerceProductModel], target_woocommerce_category_name: str
    ) -> bool:

        for woocommerce_product_model in woocommerce_product_models:
            if target_woocommerce_category_name is not None:
                target_woocommerce_category_model = WoocommerceCategoryModel(name=target_woocommerce_category_name)
                woocommerce_product_model.categories = [target_woocommerce_category_model]

            woocommerce_product_model = self.resolve_or_upload(woocommerce_product_model=woocommerce_product_model)

            self.waiting(1000)

# in vartion misazim



        
            for row in woocommerce_product_model.attributes:

                variation_attributes = []

                for attribute_name, option in row.items():

                    attribute_id = attribute_ids.get(
                        attribute_name
                    )

                    if not attribute_id:
                        continue

                    variation_attributes.append(
                        WoocommerceVariationAttributeModel(
                            id=attribute_id,
                            name=attribute_name,
                            option=option,
                        )
                    )

                variation_model = WoocommerceVariationModel(
                    attributes=variation_attributes,
                    regular_price=woocommerce_product_model.regular_price,
                    price=woocommerce_product_model.price,
                    manage_stock=True,
                    stock_status="instock",
                )

                self.woocommerce_product.upload_variation(
                    product_id=woocommerce_product_model.id,
                    variation_model=variation_model,
                )










        self.woocommerce_rollback.rollback()

        return True

    #  --
    #  ...
    #  --

    def resolve_or_upload(self, woocommerce_product_model: WoocommerceProductModel)->WoocommerceProductModel:
        try:
            product = self.woocommerce_product.get_product_by_name(woocommerce_product_model.name)

            woocommerce_categories_model: list[WoocommerceCategoryModel] = []
            woocommerce_brands_model: list[WoocommerceBrandModel] = []
            woocommerce_tags_model: list[WoocommerceTagModel] = []
            woocommerce_images_model: list[WoocommerceImageModel] = []
            woocommerce_product_attribute_models: list[WoocommerceProductAttributeModel] = []

            if product:
                return product

            woocommerce_image = WoocommerceImage()
            for image in woocommerce_product_model.images:
                woocommerce_images_model.append(woocommerce_image.resolve_or_upload(image))
                self.woocommerce_session_model.add_media(image)

            woocommerce_category = WoocommerceCategory()
            for category in woocommerce_product_model.categories:
                woocommerce_categories_model.append(woocommerce_category.resolve_or_upload(category))
                self.woocommerce_session_model.add_category(category)

            woocommerce_brand = WoocommerceBrand()
            for brand in woocommerce_product_model.brands:
                if not brand.name:
                    brand.name = "NoBrand"
                woocommerce_brands_model.append(woocommerce_brand.resolve_or_upload(brand))
                self.woocommerce_session_model.add_brand(brand)

            woocommerce_tag = WoocommerceTag()
            for tag in woocommerce_product_model.tags:
                woocommerce_tags_model.append(woocommerce_tag.resolve_or_upload(tag))
                self.woocommerce_session_model.add_tag(tag)

            woocommerce_attribute = WoocommerceAttribute()
            for woocommerce_product_attribute_model in woocommerce_product_model.attributes:
                woocommerce_attribute_model = woocommerce_attribute.resolve_or_upload(
                    WoocommerceAttributeModel(name=woocommerce_product_attribute_model.name)
                )

                for woocommerce_attribute_term_model in woocommerce_product_attribute_model.options:
                    woocommerce_attribute.resolve_or_upload_term(
                        attribute_id=woocommerce_attribute_model.id,
                        term_model=WoocommerceAttributeTermModel(name=woocommerce_attribute_term_model),
                    )

                woocommerce_product_attribute_models.append(woocommerce_product_attribute_model)

            # session ezafeh beshe

            woocommerce_product_model.images = woocommerce_images_model
            woocommerce_product_model.categories = woocommerce_categories_model
            woocommerce_product_model.brands = woocommerce_brands_model
            woocommerce_product_model.tags = woocommerce_tags_model
            woocommerce_product_model.attributes = woocommerce_product_attribute_models

            woocommerce_product_model = remove_none(woocommerce_product_model)
            woocommerce_product_model = self.woocommerce_product.upload_product(woocommerce_product_model)

            self.woocommerce_session_model.add_product(woocommerce_product_model)

            return woocommerce_product_model

        except Exception as exp:
            self.error(f"resolve_or_upload: {exp}")

    #  --
    #  ...
    #  --

    def fetch_from_woocommerce(self, search_in_woocommerce_model: SearchInWoocommerceModel) -> WoocommerceProductModel:
        woocommerce_product_models = self.woocommerce_product.get_product_by_search_in_woocommerce_model(
            search_in_woocommerce_model=search_in_woocommerce_model
        )
        return woocommerce_product_models
