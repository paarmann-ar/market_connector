from typing import Any
from apis.core.base import Base

# --
# ...
# --


class BaseZalandoLoungeApi(Base):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

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
