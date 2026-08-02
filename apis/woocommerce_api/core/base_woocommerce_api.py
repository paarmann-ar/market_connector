from typing import Any

import colorama

import CONSTS
from apis.core.base import Base
from services.connection.connection_provider import ConnectionProvider
from apis.woocommerce_api.models.woocommerce_session_model import WoocommerceSessionModel

# --
# ...
# --


class BaseWoocommerceApi(Base):
    def __init__(self, **kwargs: Any) -> None:
        pass

    # --
    # ...
    # --

    def __new__(cls, **kwargs: Any):

        if hasattr(cls, "instance_args"):
            if cls.instance_args != kwargs:
                cls.instance = None

        if not hasattr(cls, "instance") or not cls.instance:
            cls.instance = super().__new__(cls)

            cls.instance_args = kwargs

            cls.request = ConnectionProvider().request

            cls.instance.config_dictionary = cls.get_config_dictionary()

        cls.prompt_on_screen(f"{__class__.__name__}, {id(cls.instance)}")
        return cls.instance

    # --
    # ...
    # --

    def __call__(self) -> str:
        return self.instance

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls) -> str:
        return ""

    # --
    # ...
    # --

    @classmethod
    def prompt_on_screen(cls, message="") -> str:
        colorama.init()
        print(f"{CONSTS.COLORS.AQUA_PROMPT.value}{message}{CONSTS.COLORS.ENDC.value}")
