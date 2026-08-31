from apis.apis_provider import ApisProvider
from apis.woocommerce_api.models.woocommerce_product_model import WoocommerceProductModel
from app.core.base import Base

# --
# ...
# --


class SetupMarketConnectorController(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.apis_provider = ApisProvider()
        self.woocommerce_product_models: list[WoocommerceProductModel] = []

    #  --
    #  ...
    #  --

    def register_user_token(self):
        self.apis_provider.ebay_api.ebay_token_api.register_user_token()
