from apis.ebay_api.ebay_api import EbayApi
from apis.woocommerce_api.models.woocommerce_brand_model import WoocommerceBrandModel
from apis.woocommerce_api.models.woocommerce_category_model import WoocommerceCategoryModel
from apis.woocommerce_api.models.woocommerce_image_model import WoocommerceImageModel
from apis.woocommerce_api.models.woocommerce_product_model import WoocommerceProductModel
from apis.woocommerce_api.models.woocommerce_session_model import WoocommerceSessionModel
from apis.woocommerce_api.services.woocommerce_uploader import WoocommerceUploader
from apis.woocommerce_api.models.woocommerce_tag_model import WoocommerceTagModel
from apis.woocommerce_api.woocommerce_api import WoocommerceApi
from apis.wordpress_api.models.wordpress_media_model import WordpressMediaModel
from apis.wordpress_api.wordpress_api import WordpressApi
from toolboxs.decorators import singleton

# --
# ...
# --


@singleton
class ApisProvider:
    def __init__(self, **kwargs):

        self.wordpress_api = WordpressApi().instance
        self.ebay_api = EbayApi().instance
        self.woocommerce_api = WoocommerceApi().instance
