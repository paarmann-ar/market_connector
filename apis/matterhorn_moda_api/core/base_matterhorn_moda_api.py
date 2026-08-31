from typing import Any

from apis.core.base import Base

# --
# ...
# --


class BaseMatterhornModaApi(Base):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        self.config_dictionary = self.get_config_dictionary()

        # cache
        self.product_matterhorn_moda_models_cache: list[object] = None

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    #  --
    #  ...
    #  --

    def __call__(self) -> str:
        return self

    #  --
    #  ...
    #  --

    @classmethod
    def get_config_dictionary(cls) -> str:
        return ""
