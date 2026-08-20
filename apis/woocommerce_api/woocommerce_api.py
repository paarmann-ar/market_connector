from typing import TYPE_CHECKING

from apis.woocommerce_api.config.woocommerce_api_config import WoocommerceApiConfig
from apis.woocommerce_api.core.base_woocommerce_api import BaseWoocommerceApi
from apis.woocommerce_api.create_product_seo import CreateProductSeo
from apis.woocommerce_api.models.woocommerce_product_model import WoocommerceProductModel
from toolboxs.numbers import Numbers
from toolboxs.text import Text

if TYPE_CHECKING:
    from apis.ebay_api.models.browse.product_ebay_model import ProductEbayModel

# --
# ...
# --


class WoocommerceApi(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.create_product_seo = CreateProductSeo()
        self.create_product_seo.rank_math_model = self.rank_math_model

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
        target_woocommerce_category_model = self.woocommerce_service_provider.woocommerce_category_model(
            name=target_woocommerce_category_name
        )

        for woocommerce_product_model in woocommerce_product_models:
            woocommerce_product_model.categories = [target_woocommerce_category_model]

            self.woocommerce_service_provider.woocommerce_uploader.resolve_or_upload(woocommerce_product_model=woocommerce_product_model)

            self.waiting(1000)

        self.woocommerce_service_provider.woocommerce_rollback.rollback()

        return True
