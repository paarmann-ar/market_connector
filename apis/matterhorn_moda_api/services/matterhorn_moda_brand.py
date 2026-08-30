from apis.matterhorn_moda_api.models.brand_matterhorn_moda_model import BrandMatterhornModaModel
from apis.matterhorn_moda_api.core.base_matterhorn_moda_api import BaseMatterhornModaApi
from apis.matterhorn_moda_api.config.matterhorn_moda_api_config import (
    MatterhornModaApiConfig,
)

# --
# ...
# --


class MatterhornModaBrand(BaseMatterhornModaApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.base_url = self.config_dictionary.get("base_url", None)
        self.brand_url = self.config_dictionary.get("brand_url", None)
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

    def get_brand_matterhorn_moda_models(self) -> list[BrandMatterhornModaModel]:

        try:
            response = self.request(
                method="get",
                url=f"{self.base_url}{self.brand_url}",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"{self.api_key}",
                },
            )

            brand_matterhorn_moda_models: list[BrandMatterhornModaModel] = []

            for item in response:
                brand_matterhorn_moda_models.append(BrandMatterhornModaModel(**item))

            return brand_matterhorn_moda_models

        except Exception as exp:
            self.prompt_on_screen(f"get_brand_matterhorn_moda_models: {exp}")
