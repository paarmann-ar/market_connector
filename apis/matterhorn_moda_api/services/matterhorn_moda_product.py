from apis.matterhorn_moda_api.config.matterhorn_moda_api_config import (
    MatterhornModaApiConfig,
)
from apis.matterhorn_moda_api.core.base_matterhorn_moda_api import BaseMatterhornModaApi
from apis.matterhorn_moda_api.models.product_matterhorn_moda_model import ProductMatterhornModaModel
from apis.matterhorn_moda_api.models.fetch_matterhorn_moda_config_model import FetchMatterhornModaConfigModel

# --
# ...
# --


class MatterhornModaProduct(BaseMatterhornModaApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.base_url = self.config_dictionary.get("base_url", None)

        self.product_url = self.config_dictionary.get("product_url", None)

        self.api_key = self.config_dictionary.get("api_key", None)

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    #  --
    #  ...
    #  --

    @classmethod
    def get_config_dictionary(cls):
        return MatterhornModaApiConfig().get_dictionary()

    #  --
    #  ...
    #  --

    def get_products_matterhorn_moda_models(
        self, fetch_matterhorn_moda_config_model: FetchMatterhornModaConfigModel, page=1
    ) -> list[ProductMatterhornModaModel]:

        try:
            # if self.product_matterhorn_moda_models_cache:
            #     return self.product_matterhorn_moda_models_cache

            response = self.request(
                method="get",
                url=f"{self.base_url}{self.product_url}/?page={page}&active=true&stock_total>0",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"{self.api_key}",
                },
            )

            product_matterhorn_moda_models: list[ProductMatterhornModaModel] = []

            for item in response:
                product_matterhorn_moda_model = ProductMatterhornModaModel(**item)
                product_matterhorn_moda_model.attribute = fetch_matterhorn_moda_config_model.attribute_name

                product_matterhorn_moda_models.append(product_matterhorn_moda_model)

            self.product_matterhorn_moda_models_cache.extend(product_matterhorn_moda_models)

            return product_matterhorn_moda_models

        except Exception as exp:
            self.prompt_on_screen(f"get_products_matterhorn_moda_models: {exp}")
