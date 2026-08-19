import os

from apis.apis_provider import ApisProvider
from apis.ebay_api.models.search_in_ebay_model import SearchInEbayModel
from apis.woocommerce_api.models.woocommerce_product_model import WoocommerceProductModel
from apis.wordpress_api.models.wordpress_media_model import WordpressMediaModel
from app.core.base import Base
from image_services.models.image_data_model import ImageDataModel
from toolboxs.file_and_folder_operation import FileAndFolderOperation
from apis.ebay_api.models.browse.product_ebay_model import ProductEbayModel

# --
# ...
# --


class SetupMarketConnectorController(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.apis_provider = ApisProvider()
        self.woocommerce_product_models: list[WoocommerceProductModel] = []

    # --
    # ...
    # --

    def register_user_token(self):
        self.apis_provider.ebay_api.ebay_token_api.register_user_token()
