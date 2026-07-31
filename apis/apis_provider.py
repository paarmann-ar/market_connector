from toolboxs.decorators import singleton
from apis.wordpress_api.wordpress_api.wordpress_api import WordpressApi
from apis.ebay_api.ebay_api.ebay_api import EbayApi
from apis.woocommerce_api.woocommerce_api.woocommerce_api import WoocommerceApi
from apis.models.woocommerce_product_model import WoocommerceProductModel
from apis.models.woocommerce_category_model import WoocommerceCategoryModel
from apis.models.woocommerce_image_model import WoocommerceImageModel
from apis.models.wordpress_media_model import WordpressMediaModel
# --
# ...
# --
@singleton
class ApisProvider:
    def __init__(self, **kwargs):

        self.wordpress_api = WordpressApi().instance
        self.ebay_api = EbayApi().instance
        self.woocommerce_api = WoocommerceApi().instance
        self.woocommerce_product_model = WoocommerceProductModel
        self.woocommerce_category_model = WoocommerceCategoryModel
        self.woocommerce_image_model = WoocommerceImageModel
        self.wordpress_media_model = WordpressMediaModel

