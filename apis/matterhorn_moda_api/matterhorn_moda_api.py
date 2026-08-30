from apis.matterhorn_moda_api.core.base_matterhorn_moda_api import BaseMatterhornModaApi
from apis.matterhorn_moda_api.config.matterhorn_moda_api_config import MatterhornModaApiConfig
from apis.matterhorn_moda_api.models.product_matterhorn_moda_model import ProductMatterhornModaModel
from apis.matterhorn_moda_api.services.matterhorn_moda_product import MatterhornModaProduct
from apis.matterhorn_moda_api.services.matterhorn_moda_category  import MatterhornModaCategory
from apis.matterhorn_moda_api.services.matterhorn_moda_brand  import MatterhornModaBrand



# --
# ...
# --


class MatterhornModaApi(BaseMatterhornModaApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.matterhorn_moda_product = MatterhornModaProduct()
        self.matterhorn_moda_category = MatterhornModaCategory()
        self.matterhorn_moda_brand = MatterhornModaBrand()

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

    def pipeline_fetch_products_from_matterhorn_moda(self) -> list[ProductMatterhornModaModel]:
        product_matterhorn_moda_model = self.matterhorn_moda_product.get_products_matterhorn_moda_models()

        return product_matterhorn_moda_model

    # --
    # ...
    # --
