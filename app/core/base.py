from abc import ABC
from typing import Any
from apis.core.singleton_meta import SingletonMeta

from app.core.config.base_config import BaseConfig
from app.core.prompt_on_screen import PromptOnScreen
from apis.core.waiting import Wating
from services.disk.json.json_manager import JSONManager
from services.logging.log_provider import LogProvider
from services.mail.email_provider import EMailProvider
from image_services.image_provider.image_provider import ImageProvider

# --
# ...
# --


class Base(ABC, metaclass=SingletonMeta):
    state = {}

    def __init__(self, **kwargs: Any) -> None:

        self.waiting = Wating()

        self.mail = EMailProvider().email

        self.info = LogProvider().info
        self.error = LogProvider().error
        self.stack = LogProvider().stack

        self.json = JSONManager()
        self.image_provider = ImageProvider()

        self.config_dictionary = self.get_config_dictionary()

        self.prompt_on_screen = PromptOnScreen()

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(self) -> str:
        return BaseConfig().get_dictionary()

    # --
    # ...
    # --

    @classmethod
    def get_elements(self) -> str:
        return None
