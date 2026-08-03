from abc import ABC
from typing import Any

from apis.core.prompt_on_screen import PromptOnScreen
from apis.core.singleton_meta import SingletonMeta
from apis.core.waiting import Wating
from services.disk.service_disk_provider import ServiceDiskProvider

# --
# ...
# --


class Base(ABC, metaclass=SingletonMeta):
    def __init__(self, **kwargs: Any) -> None:

        self.waiting = Wating()
        self.prompt_on_screen = PromptOnScreen()

        # create instance for loging
        self.info = kwargs.get("log_info_class", "log_info_class")
        self.error = kwargs.get("log_error_class", "log_error_class")
        self.config_dictionary = self.get_config_dictionary()

        # working with file
        self.json = ServiceDiskProvider().json
        self.csv = ServiceDiskProvider().csv

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
