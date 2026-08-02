from apis.woocommerce_api.config.woocommerce_api_config import (
    WoocommerceApiConfig,
)
from apis.woocommerce_api.core.base_woocommerce_api import (
    BaseWoocommerceApi,
)
from apis.woocommerce_api.services.woocommerce_tag_parser import WoocommerceTagPaser

from apis.woocommerce_api.models.woocommerce_brand_model import WoocommerceBrandModel
from apis.woocommerce_api.models.woocommerce_category_model import WoocommerceCategoryModel
from apis.woocommerce_api.models.woocommerce_image_model import WoocommerceImageModel
from apis.woocommerce_api.models.woocommerce_product_model import WoocommerceProductModel
from apis.woocommerce_api.models.woocommerce_session_model import WoocommerceSessionModel
from apis.woocommerce_api.models.woocommerce_tag_model import WoocommerceTagModel
from apis.woocommerce_api.services.woocommerce_uploader import WoocommerceUploader
from apis.woocommerce_api.services.woocommerce_rollback import WoocommerceRollback
from toolboxs.decorators import singleton

# --
# ...
# --


@singleton
class WoocommerceApi(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:

        self.woocommerce_uploader = WoocommerceUploader()
        self.woocommerce_product_model = WoocommerceProductModel
        self.woocommerce_tag_model = WoocommerceTagModel
        self.woocommerce_brand_model = WoocommerceBrandModel
        self.woocommerce_category_model = WoocommerceCategoryModel
        self.woocommerce_image_model = WoocommerceImageModel
        self.woocommerce_session_model = WoocommerceSessionModel
        self.woocommerce_tag_parser = WoocommerceTagPaser
        self.woocommerce_rollback = WoocommerceRollback()

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
