from abc import ABC
from typing import Any

from apis.core.prompt_on_screen import PromptOnScreen
from apis.core.singleton_meta import SingletonMeta
from apis.core.waiting import Wating
from services.disk.service_disk_provider import ServiceDiskProvider
from services.connection.connection_provider import ConnectionProvider
from services.logging.log_provider import LogProvider
from ki.prompt_provider.prompt_manager import PromptManager
from ki.core.cache import Cache
# --
# ...
# --


class Base(ABC, metaclass=SingletonMeta):
    def __init__(self, **kwargs: Any) -> None:

        self.waiting = Wating()
        self.prompt_on_screen = PromptOnScreen()

        # create instance for loging
        self.info = LogProvider().info
        self.error = LogProvider().error
        self.config_dictionary = self.get_config_dictionary()

        # working with file
        self.json = ServiceDiskProvider().json
        self.csv = ServiceDiskProvider().csv

        self.request = ConnectionProvider().request

        self.cache = Cache()
        self.prompt_manager = PromptManager()

    # --
    # ...
    # --

    def __call__(self) -> str:
        return self

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(self) -> str:
        return ""
