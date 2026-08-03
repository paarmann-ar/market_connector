from apis.ebay_api.ebay_api import EbayApi
from apis.woocommerce_api.woocommerce_api import WoocommerceApi
from apis.wordpress_api.wordpress_api import WordpressApi
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
