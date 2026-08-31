from apis.matterhorn_moda_api.config.matterhorn_moda_api_config import (
    MatterhornModaApiConfig,
)
from apis.matterhorn_moda_api.core.base_matterhorn_moda_api import BaseMatterhornModaApi
from apis.matterhorn_moda_api.models.product_matterhorn_moda_model import ProductMatterhornModaModel
from apis.matterhorn_moda_api.services.matterhorn_size_table_parser import MatterhornSizeTableParser

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

    def get_products_matterhorn_moda_models(self) -> list[ProductMatterhornModaModel]:

        try:
            if self.product_matterhorn_moda_models_cache:
                return self.product_matterhorn_moda_models_cache

            response = self.request(
                method="get",
                url=f"{self.base_url}{self.product_url}/?page=1",
                headers={
                    "Accept": "application/json",
                    "Authorization": f"{self.api_key}",
                },
            )

            product_matterhorn_moda_models: list[ProductMatterhornModaModel] = []

            for item in response:
                product_matterhorn_moda_model = ProductMatterhornModaModel(**item)

                #product_matterhorn_moda_model.attribute = MatterhornSizeTableParser.parse(product_matterhorn_moda_model.size_table_html)








                product_matterhorn_moda_model.attribute = MatterhornSizeTableParser.parse_rows(product_matterhorn_moda_model.size_table_html)








                product_matterhorn_moda_models.append(product_matterhorn_moda_model)

            self.product_matterhorn_moda_models_cache = product_matterhorn_moda_models

            return product_matterhorn_moda_models

        except Exception as exp:
            self.prompt_on_screen(f"get_products: {exp}")
