from abc import ABC
from typing import Any

from app.core.config.base_config import BaseConfig
from app.core.prompt_on_screen import PromptOnScreen
from services.disk.json.json_manager import JSONManager
from services.logging.log_provider import LogProvider
from services.mail.email_provider import EMailProvider

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

            cls.instance.json = JSONManager()

            cls.instance.config_dictionary = cls.get_config_dictionary()

            cls.prompt_on_screen = PromptOnScreen()

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
        return BaseConfig().get_dictionary()

    # --
    # ...
    # --

    @classmethod
    def get_elements(cls) -> str:
        return None
