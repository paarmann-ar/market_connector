from apis.matterhorn_moda_api.models.category_matterhorn_moda_model import CategoryMatterhornModaModel
from apis.matterhorn_moda_api.core.base_matterhorn_moda_api  import BaseMatterhornModaApi
from apis.matterhorn_moda_api.config.matterhorn_moda_api_config import (
    MatterhornModaApiConfig,
)

# --
# ...
# --

class MatterhornModaCategory(BaseMatterhornModaApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.base_url = self.config_dictionary.get("base_url", None)
        self.category_url = self.config_dictionary.get("category_url", None)
        self.api_key = self.config_dictionary.get("api_key", None)

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return MatterhornModaApiConfig().get_dictionary()

    # --
    # ...
    # --

    def get_category_matterhorn_moda_models(self) -> list[CategoryMatterhornModaModel]:

        try:
            response = self.request(
                method="get",
                url=f"{self.base_url}{self.category_url}",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"{self.api_key}",
                },
            )

            category_matterhorn_moda_models: list[CategoryMatterhornModaModel] = []

            for item in response:
                category_matterhorn_moda_models.append(CategoryMatterhornModaModel(**item))

            return category_matterhorn_moda_models

        except Exception as exp:
            self.prompt_on_screen(f"get_category_matterhorn_moda_models: {exp}")
