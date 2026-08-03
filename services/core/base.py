from abc import ABC
from typing import Any

from apis.core.prompt_on_screen import PromptOnScreen
from apis.core.singleton_meta import SingletonMeta
from apis.core.waiting import Wating

# --
# ...
# --


class Base(ABC, metaclass=SingletonMeta):
    def __init__(self, **kwargs: Any) -> None:

        self.waiting = Wating()
        self.prompt_on_screen = PromptOnScreen()

        # create instance for loging
        self.config_dictionary = self.get_config_dictionary()

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
