from typing import Any

from apis.core.base import Base
from apis.woocommerce_api.models.woocommerce_session_model import (
    WoocommerceSessionModel,
)
from apis.woocommerce_api.services.woocommerce_service_provider import (
    WoocommerceServiceProvider,
)
from apis.seo_api.models.rank_math_model import RankMathModel

# --
# ...
# --


class BaseWoocommerceApi(Base):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.woocommerce_service_provider = WoocommerceServiceProvider()
        self.woocommerce_session_model = WoocommerceSessionModel()

        self.rank_math_model = RankMathModel()

        self.config_dictionary = self.get_config_dictionary()

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    # --
    # ...
    # --

    def __call__(self) -> str:
        return self

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls) -> str:
        return ""
