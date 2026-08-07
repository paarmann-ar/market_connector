from apis.apis_provider import ApisProvider
from apis.ebay_api.models.search_in_ebay_model import SearchInEbayModel
from app.core.base import Base

# --
# ...
# --


class MarketConnectorController(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.apis_provider = ApisProvider()
        self.woocommerce_product_models = []

    # --
    # ...
    # --

    def fetch_from_ebay(self, search_in_ebay_model: SearchInEbayModel):
        self.apis_provider.ebay_api.fetch_product_from_ebay_by_search_in_ebay_model(search_in_ebay_model)

    # --
    # ...
    # --

    def convert_ebay_to_woocommerce_product_model(self, price_anpassen) -> None:
        ebay_product_detail_model_list = self.apis_provider.ebay_api.product_detail_list
        self.apis_provider.woocommerce_api.convert_ebay_product_model_to_woocommerce_product_model(
            ebay_product_detail_model_list=ebay_product_detail_model_list,
            price_anpassen=price_anpassen,
        )

    # --
    # ...
    # --

    def upload_model_to_woocommerce(self, target_woocommerce_category_name: str) -> bool:
        self.apis_provider.woocommerce_api.upload_product_model_to_woocommerce(target_woocommerce_category_name)
