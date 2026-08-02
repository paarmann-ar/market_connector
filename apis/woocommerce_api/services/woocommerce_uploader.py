from apis.woocommerce_api.services.woocommerce_category import WoocommerceCategory

from apis.woocommerce_api.config.woocommerce_api_config import (
    WoocommerceApiConfig,
)
from apis.woocommerce_api.core.base_woocommerce_api import (
    BaseWoocommerceApi,
)
from apis.woocommerce_api.services.woocommerce_product import WoocommerceProduct
from apis.woocommerce_api.models.woocommerce_brand_model import WoocommerceBrandModel
from apis.woocommerce_api.models.woocommerce_category_model import WoocommerceCategoryModel
from apis.woocommerce_api.models.woocommerce_image_model import WoocommerceImageModel
from apis.woocommerce_api.models.woocommerce_product_model import WoocommerceProductModel
from apis.woocommerce_api.models.woocommerce_tag_model import WoocommerceTagModel
from apis.woocommerce_api.services.woocommerce_brand import WoocommerceBrand
from apis.woocommerce_api.services.woocommerce_image import WoocommerceImage
from apis.woocommerce_api.services.woocommerce_tag import WoocommerceTag
from toolboxs.dict_utils import remove_none

# --
# ...
# --


class WoocommerceUploader(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:
        self.base_url = self.instance.config_dictionary.get("base_url")
        self.wp_media_url = self.instance.config_dictionary.get("wp_media_url")

        self.consumer_key = self.instance.config_dictionary.get("consumer_key")
        self.consumer_secret = self.instance.config_dictionary.get("consumer_secret")

        self.wp_user = self.instance.config_dictionary.get("wp_user")
        self.wp_password = self.instance.config_dictionary.get("wp_password")

        self.products_url = self.instance.config_dictionary.get("products_url")
        self.woocommerce_product = WoocommerceProduct()

        self.prompt_on_screen(f"{__class__.__name__}, {id(__class__)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return WoocommerceApiConfig().instance.dictionary

    # --
    # ...
    # --

    def __call__(self) -> str:
        pass

    # --
    # ...
    # --

    def resolve_or_upload(self, product_model: WoocommerceProductModel):
        try:
            product = self.woocommerce_product.get_product_by_name(product_model.name)

            woocommerce_categories_model: list[WoocommerceCategoryModel] = []
            woocommerce_brands_model: list[WoocommerceBrandModel] = []
            woocommerce_tags_model: list[WoocommerceTagModel] = []
            woocommerce_images_model: list[WoocommerceImageModel] = []

            if product:
                return product

            woocommerce_image = WoocommerceImage()
            for image in product_model.images:
                woocommerce_images_model.append(woocommerce_image.resolve_or_upload(image))
                # self.woocommerce_session_model.add_media(image)

            woocommerce_category = WoocommerceCategory()
            for category in product_model.categories:
                woocommerce_categories_model.append(
                    woocommerce_category.resolve_or_upload(category)
                )
                # self.woocommerce_session_model.add_category(category)

            woocommerce_brand = WoocommerceBrand()
            for brand in product_model.brands:
                woocommerce_brands_model.append(woocommerce_brand.resolve_or_upload(brand))
                # self.woocommerce_session_model.add_brand(brand)

            woocommerce_tag = WoocommerceTag()
            for tag in product_model.tags:
                woocommerce_tags_model.append(woocommerce_tag.resolve_or_upload(tag))
                # self.woocommerce_session_model.add_tag(tag)

            product_model.images = woocommerce_images_model
            product_model.categories = woocommerce_categories_model
            product_model.brands = woocommerce_brands_model
            product_model.tags = woocommerce_tags_model

            product_model = remove_none(product_model)
            self.woocommerce_product.upload_product(WoocommerceProductModel(**product_model))

            # self.woocommerce_session_model.add_product(product_model)

        except Exception as exp:
            print(f"resolve_or_upload: {exp}")
