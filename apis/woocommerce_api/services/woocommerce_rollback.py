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

    #  --
    #  ...
    #  --

    @classmethod
    def get_config_dictionary(cls):
        return WoocommerceApiConfig().get_dictionary()

    #  --
    #  ...
    #  --

    def __call__(self) -> str:
        self.rollback()

    #  --
    #  ...
    #  --

    def rollback(self):
        try:
            pass

        except Exception as exp:
            self.prompt_on_screen(f"rollback: {exp}")
