from apis.ebay_api.ebay_api import EbayApi
from apis.matterhorn_moda_api.matterhorn_moda_api import MatterhornModaApi
from apis.woocommerce_api.woocommerce_api import WoocommerceApi
from apis.wordpress_api.wordpress_api import WordpressApi
from apis.zalando_lounge_api.zalando_lounge_api import ZalandoLoungeApi
from toolboxs.decorators import singleton

# --
# ...
# --


@singleton
class ApisProvider:
    def __init__(self, **kwargs):

        self.wordpress_api = WordpressApi()
        self.ebay_api = EbayApi()
        self.woocommerce_api = WoocommerceApi()
        self.zalando_lounge_api = ZalandoLoungeApi()
        self.matterhorn_moda_api = MatterhornModaApi()
