from typing import Any
from abc import ABC, abstractmethod
from services.disk.json.json_manager import JSONManager
import CONSTS
from collections import namedtuple
from services.mail.email_provider import EMailProvider
from services.log_.log_provider import LogProvider
import CONSTS
import colorama
from app.core.config.base_config import BaseConfig
from apis.apis_provider import ApisProvider

# --
# ...
# --


class Base(ABC):
    state = {}

    def __new__(cls, *args, **kwargs: Any):

        if hasattr(cls, "instance_args"):
            if cls.instance_args != kwargs:
                cls.instance = None

        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
            cls.state["base_id"] = id(cls)

            cls.instance_args = kwargs

            cls.aqua_result = []

            cls.instance.mail = EMailProvider().email

            cls.instance.info = LogProvider().info
            cls.instance.error = LogProvider().error
            cls.instance.stack = LogProvider().stack

            cls.instance.json = JSONManager().instance

            cls.ebay = ApisProvider().ebay_api
            cls.woocommerce = ApisProvider().woocommerce_api
            cls.wordpress = ApisProvider().wordpress_api

            cls.woocommerce_product_model = ApisProvider().woocommerce_product_model
            cls.woocommerce_category_model = ApisProvider().woocommerce_category_model
            cls.woocommerce_image_model = ApisProvider().woocommerce_image_model
            cls.wordpress_media_model = ApisProvider().wordpress_media_model

            cls.instance.config_dictionary = cls.get_config_dictionary()

        cls.prompt_on_screen(f"{__class__.__name__}, {id(cls.instance)}")
        return cls.instance

    # --
    # ...
    # --

    def __init__(self, *args, **kwargs: Any) -> None:
        pass

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls) -> str:
        return BaseConfig().instance.dictionary

    # --
    # ...
    # --

    @classmethod
    def get_elements(cls) -> str:
        return None

    # --
    # ...
    # --

    @classmethod
    def get_components(cls) -> str:
        return None

    # --
    # ...
    # --

    @classmethod
    def prompt_on_screen(cls, message="") -> str:
        colorama.init()
        print(
            f"{CONSTS.COLORS.INITIAL_CLASS_PROMPT.value}{message}{CONSTS.COLORS.ENDC.value}"
        )
