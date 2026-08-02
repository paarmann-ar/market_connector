from apis.woocommerce_api.config.woocommerce_api_config import (
    WoocommerceApiConfig,
)
from apis.woocommerce_api.core.base_woocommerce_api import (
    BaseWoocommerceApi,
)
from apis.woocommerce_api.services.woocommerce_brand import WoocommerceBrand
from apis.woocommerce_api.services.woocommerce_tag import WoocommerceTag
from apis.woocommerce_api.services.woocommerce_product import WoocommerceProduct
from apis.woocommerce_api.services.woocommerce_category import WoocommerceCategory

# --
# ...
# --


class WoocommerceRollback(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:

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
        self.rollback()

    # --
    # ...
    # --

    def rollback(self):
        try:
            for brand in self.woocommerce_api.woocommerce_session_model.brands:
                WoocommerceBrand().delete_brand_by_brand_id(brand.id)

            for tag in self.woocommerce_api.woocommerce_session_model.tags:
                WoocommerceTag().delete_tag_by_tag_id(tag.id)

            for product in self.woocommerce_api.woocommerce_session_model.products:
                WoocommerceProduct().delete_product_by_product_id(product.id)

            for category in self.woocommerce_api.woocommerce_session_model.categories:
                WoocommerceCategory().delete_category_by_category_id(category.id)

            return None

        except Exception as exp:
            print(f"rollback: {exp}")
