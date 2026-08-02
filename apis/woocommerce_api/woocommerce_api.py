from apis.woocommerce_api.config.woocommerce_api_config import (
    WoocommerceApiConfig,
)
from apis.woocommerce_api.core.base_woocommerce_api import (
    BaseWoocommerceApi,
)
from toolboxs.decorators import singleton
from apis.woocommerce_api.models.woocommerce_category_model import WoocommerceCategoryModel
from bs4 import BeautifulSoup

# --
# ...
# --


@singleton
class WoocommerceApi(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:
        self.woocommerce_product_models: list =[]

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

    def convert_ebay_product_model_to_woocommerce_product_model(
        self, ebay_product_detail_model_list: object
    ) -> None:
        for product in ebay_product_detail_model_list:
            woocommerce_categories_model: list = []
            woocommerce_brands_model: list = []
            woocommerce_tags_model: list = []
            woocommerce_images_model: list = []

            woocommerce_images_model.insert(
                0,
                self.woocommerce_service_provider.woocommerce_image_model.from_api(
                    {"src": product.get("image")["imageUrl"]}
                ),
            )
            for image_url in product.get("additionalImages", []):
                woocommerce_images_model.append(
                    self.woocommerce_service_provider.woocommerce_image_model.from_api(
                        {"src": image_url["imageUrl"]}
                    )
                )

            # chon faghat akharin category mikhastam dashteh basham
            category = product["categoryPath"].split("|")[-1]
            woocommerce_categories_model.append(
                self.woocommerce_service_provider.woocommerce_category_model(name=category)
            )

            woocommerce_brands_model.append(
                self.woocommerce_service_provider.woocommerce_brand_model(name=product["brand"])
            )

            woocommerce_tag_parser_model = self.woocommerce_service_provider.woocommerce_tag_parser.woocommerce_tag_parser(
                context=f"{product['title']} {product.get('brand')} {product.get('condition')} {product.get('sku')}"
            )

            for tag in woocommerce_tag_parser_model.tags:
                woocommerce_tag_model = self.woocommerce_service_provider.woocommerce_tag_model()
                woocommerce_tag_model.name = tag
                woocommerce_tags_model.append(woocommerce_tag_model)

            self.woocommerce_product_models.append(
                self.woocommerce_service_provider.woocommerce_product_model(
                    name=f"{product['title']} - {product['condition']}",
                    slug="",
                    permalink="",
                    catalog_visibility="visible",
                    description=BeautifulSoup(
                        product.get("description", ""), "html.parser"
                    ).get_text(separator=" ", strip=True),
                    short_description=BeautifulSoup(
                        product.get("shortDescription", ""), "html.parser"
                    ).get_text(separator=" ", strip=True),
                    sku="",
                    price=str(round(float(product["price"]["value"]) * 1.3)),
                    regular_price=str(round(float(product["price"]["value"]) * 1.3)),
                    sale_price=str(round(float(product["price"]["value"]) * 1.3)),
                    on_sale=True,
                    tax_status="taxable",
                    tax_class="",
                    manage_stock=False,
                    shipping_required=True,
                    shipping_taxable=True,
                    shipping_class="",
                    shipping_class_id=0,
                    stock_status="instock",
                    categories=woocommerce_categories_model,
                    brands=woocommerce_brands_model,
                    tags=woocommerce_tags_model,
                    images=woocommerce_images_model,
                )
            )

        self.prompt_on_screen(self.woocommerce_product_models)

    # --
    # ...
    # --

    def upload_product_model_to_woocommerce(self, target_woocommerce_category_name: str) -> bool:
        target_woocommerce_category_model = self.woocommerce_service_provider.woocommerce_category_model(name=target_woocommerce_category_name)

        for product_model in self.woocommerce_product_models:
            product_model.categories = [target_woocommerce_category_model]
            self.woocommerce_service_provider.woocommerce_uploader.resolve_or_upload(
                product_model=product_model
            )

            self.delay(1000)

        self.woocommerce_service_provider.woocommerce_rollback.rollback()
        return True
