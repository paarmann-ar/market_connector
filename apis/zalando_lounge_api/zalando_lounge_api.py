from apis.core.base import Base
from apis.zalando_lounge_api.config.zalando_lounge_api_config import ZalandoLoungeApiConfig
from apis.zalando_lounge_api.models.search_in_zalando_lounge_model import SearchInZalandoLoungeModel
from apis.zalando_lounge_api.models.zalando_lounge_product_model import ZalandoLoungeProductModel
from apis.zalando_lounge_api.services.zalando_lounge_client_api import ZalandoLoungeClientApi

# --
# ...
# --


class ZalandoLoungeApi(Base):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.zalando_lounge_client_api = ZalandoLoungeClientApi()

    #  --
    #  ...
    #  --

    @classmethod
    def get_config_dictionary(cls):
        return ZalandoLoungeApiConfig().get_dictionary()

    #  --
    #  ...
    #  --

    def fetch_from_zalando_lounge(self, search_in_zalando_lounge_model: SearchInZalandoLoungeModel) -> ZalandoLoungeProductModel:

        try:
            zalando_lounge_product_model = self.zalando_lounge_client_api.connect()
            zalando_lounge_product_model = self.zalando_lounge_client_api.get_zalando_lounge_products_by_campaign_artikel_sku(
                campaign_id=search_in_zalando_lounge_model.campaign_id, sku=search_in_zalando_lounge_model.sku
            )

            return zalando_lounge_product_model

        except Exception as exp:
            self.prompt_on_screen(f"fetch_from_zalando_lounge: {exp}")
