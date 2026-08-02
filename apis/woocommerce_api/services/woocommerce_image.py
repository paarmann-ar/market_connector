from apis.woocommerce_api.config.woocommerce_api_config import (
    WoocommerceApiConfig,
)

from apis.woocommerce_api.core.base_woocommerce_api import (
    BaseWoocommerceApi,
)
from apis.woocommerce_api.models.woocommerce_image_model import WoocommerceImageModel
from toolboxs.dict_utils import remove_none

# --
# ...
# --


class WoocommerceImage(BaseWoocommerceApi):
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

    def __call__(self, category_id) -> str:
        pass

    # --
    # ...
    # --

    def get_image_by_name(self, name: str):
        return None

    # --
    # ...
    # --

    def get_all_images(self, record_per_page: int = 100):

        try:
            return None

        except Exception as exp:
            print(f"get_all_images: {exp}")

    # --
    # ...
    # --

    def upload_image(self, image_model: WoocommerceImageModel):

        try:
            return None

        except Exception as exp:
            print(f"upload_image: {exp}")

    # --
    # ...
    # --

    def resolve_or_upload(self, woocommerce_image_model: WoocommerceImageModel):
        return remove_none(woocommerce_image_model)


def test():
    WoocommerceImage().resolve_or_upload("hahaha")
