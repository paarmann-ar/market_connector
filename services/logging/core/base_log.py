from typing import Any
from services.core.singleton_meta import SingletonMeta

# --
# ...
# --


class BaseLog(metaclass=SingletonMeta):
    def __init__(self, **kwargs: Any) -> None:

        self.template_dictionary = self.get_template_dictionary()
        self.config_dictionary = self.get_config_dictionary()

        print(f"{__class__.__name__}, {id(self)}")

    # --
    # ...
    # --

    @classmethod
    def get_template_dictionary(self) -> str:
        return ""

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(self) -> str:
        return ""

    # --
    # ...
    # --

    def __call__(self) -> str:
        return self.template
