from apis.matterhorn_moda_api.config.matterhorn_moda_api_config import MatterhornModaApiConfig
from apis.matterhorn_moda_api.core.base_matterhorn_moda_api import BaseMatterhornModaApi
from apis.matterhorn_moda_api.models.product_matterhorn_moda_model import ProductMatterhornModaModel
from apis.matterhorn_moda_api.services.matterhorn_moda_brand import MatterhornModaBrand
from apis.matterhorn_moda_api.services.matterhorn_moda_category import MatterhornModaCategory
from apis.matterhorn_moda_api.services.matterhorn_moda_product import MatterhornModaProduct
from apis.matterhorn_moda_api.models.fetch_matterhorn_moda_config_model import FetchMatterhornModaConfigModel

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

    #  --
    #  ...
    #  --

    @classmethod
    def get_config_dictionary(cls):
        return MatterhornModaApiConfig().get_dictionary()

    #  --
    #  ...
    #  --

    def pipeline_fetch_products_from_matterhorn_moda(
        self, fetch_matterhorn_moda_config_model: FetchMatterhornModaConfigModel
    ) -> list[ProductMatterhornModaModel]:

        page = 1
        fetched_product = 0
        product_matterhorn_moda_models = []

        while fetched_product < fetch_matterhorn_moda_config_model.item_to_fetch:
            self.prompt_on_screen(f"I am now in page {page} and fetched {fetched_product} products")
            
            product_matterhorn_moda_models_ = self.matterhorn_moda_product.get_products_matterhorn_moda_models(
                fetch_matterhorn_moda_config_model=fetch_matterhorn_moda_config_model,page=page
            )
            if product_matterhorn_moda_models_:
                product_matterhorn_moda_models.extend(product_matterhorn_moda_models_)
                product_matterhorn_moda_models = list(filter(lambda x: x.active and x.stock_total>0, product_matterhorn_moda_models))
                fetched_product = len(product_matterhorn_moda_models)
                page += 1
            else:
                break

        return product_matterhorn_moda_models
