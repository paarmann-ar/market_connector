from abc import ABC
from typing import Any

import colorama

import CONSTS
from apis.apis_provider import ApisProvider
from app.core.config.base_config import BaseConfig
from services.disk.json.json_manager import JSONManager
from services.log_.log_provider import LogProvider
from services.mail.email_provider import EMailProvider
from toolboxs.delay import Delay
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

            cls.delay = Delay

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
        print(f"{CONSTS.COLORS.INITIAL_CLASS_PROMPT.value}{message}{CONSTS.COLORS.ENDC.value}")
