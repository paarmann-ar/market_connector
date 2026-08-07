from apis.woocommerce_api.config.woocommerce_api_config import (
    WoocommerceApiConfig,
)
from apis.woocommerce_api.core.base_woocommerce_api import (
    BaseWoocommerceApi,
)

# --
# ...
# --


class WoocommerceRollback(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

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

    def __call__(self) -> str:
        self.rollback()

    # --
    # ...
    # --

    def rollback(self):
        try:
            for brand in self.woocommerce_session_model.brands:
                self.woocommerce_service_provider.woocommerce_brand.delete_brand_by_brand_id(brand.id)

            for tag in self.woocommerce_session_model.tags:
                self.woocommerce_service_provider.woocommerce_tag.delete_tag_by_tag_id(tag.id)

            for product in self.woocommerce_session_model.products:
                self.woocommerce_service_provider.woocommerce_product.delete_product_by_product_id(product.id)

            for category in self.woocommerce_session_model.categories:
                self.woocommerce_service_provider.woocommerce_category.delete_category_by_category_id(category.id)

            return None

        except Exception as exp:
            self.prompt_on_screen(f"rollback: {exp}")
