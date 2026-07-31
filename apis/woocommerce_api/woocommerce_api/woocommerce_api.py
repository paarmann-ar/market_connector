from apis.woocommerce_api.woocommerce_api.core.base_woocommerce_api import BaseWoocommerceApi
from apis.woocommerce_api.woocommerce_api.config.woocommerce_api_config import (
    WoocommerceApiConfig,
)
from apis.woocommerce_api.woocommerce_api.core.woocommerce_product import WoocommerceProduct
from toolboxs.decorators import singleton
import CONSTS

# --
# ...
# --


@singleton
class WoocommerceApi(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:

        self.woocommerce_product = WoocommerceProduct()

        self.prompt_on_screen(f"{__class__.__name__}, {id(__class__)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return WoocommerceApiConfig().instance.dictionary

    # --
    # ...
    # --

    def get_ebay_category_id(self, marketplace_id, category_name_candidate) -> str:
        
        try:
                
            category_id_candidate = {}
            category_tree_id = self.ebay_category.get_default_category_tree_id_with_marketplace_id(marketplace_id= marketplace_id)
            category_tree = self.ebay_category.get_category_tree(category_tree_id=category_tree_id)

            self.recursive_category(category_node=category_tree)

            for category_id, category_name in self.category_dict.items():
                if category_name == category_name_candidate:
                    category_id_candidate[int(category_id)]=category_name

            self.prompt_on_screen(f"category id: {category_id_candidate}")

            return category_id_candidate

        except Exception as exp:
            print(f"get_ebay_category_id: {exp}")

    # --
    # ...
    # --
