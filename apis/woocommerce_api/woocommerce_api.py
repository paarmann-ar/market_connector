from apis.woocommerce_api.config.woocommerce_api_config import (
    WoocommerceApiConfig,
)
from apis.woocommerce_api.core.base_woocommerce_api import (
    BaseWoocommerceApi,
)
from toolboxs.numbers import Numbers
from apis.woocommerce_api.create_product_seo import CreateProductSeo
from apis.woocommerce_api.models.woocommerce_product_model import WoocommerceProductModel
from toolboxs.text import Text
# --
# ...
# --


class WoocommerceApi(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.woocommerce_product_models: list = []
        self.create_product_seo = CreateProductSeo()
        self.create_product_seo.rank_math_model = self.rank_math_model

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return WoocommerceApiConfig().get_dictionary()

    # --
    # ...
    # --

    def convert_ebay_product_model_to_woocommerce_product_model(
        self, ebay_product_detail_model_list: object, price_anpassen: float
    ) -> list[WoocommerceProductModel]:

        for product in ebay_product_detail_model_list:
            woocommerce_categories_model: list = []
            woocommerce_brands_model: list = []
            woocommerce_tags_model: list = []
            woocommerce_images_model: list = []

            ki_dict = self.create_product_seo.use_ki_to_rewrite_metadata_to_woocommerce(product=product)

            alt_image_constructor = " ".join(ki_dict.get("focus_keywords", ["_", "_"]))
            image_alt = Text().remove_dublicate_words_from_string(alt_image_constructor)
            image_alt_main = ki_dict.get("title").split("|")[0]

            self.ziel_woocommerce_product_model = self.woocommerce_service_provider.woocommerce_product_model()

            woocommerce_images_model.insert(
                0,
                self.woocommerce_service_provider.woocommerce_image_model.from_api(
                    {"src": product.get("image")["imageUrl"], "alt": image_alt_main, "is_main_image": True}
                ),
            )
            for image_url in product.get("additionalImages", []):
                woocommerce_images_model.append(
                    self.woocommerce_service_provider.woocommerce_image_model.from_api({"src": image_url.get("imageUrl"), "alt": image_alt})
                )

            # chon faghat akharin category mikhastam dashteh basham
            category = product.get("categoryPath").split("|")[-1]
            woocommerce_categories_model.append(self.woocommerce_service_provider.woocommerce_category_model(name=category))

            woocommerce_brands_model.append(self.woocommerce_service_provider.woocommerce_brand_model(name=product.get("brand")))

            woocommerce_tag_parser_model = self.woocommerce_service_provider.woocommerce_tag_parser.woocommerce_tag_parser(
                context=f"{product.get('title')} {product.get('brand')} {product.get('condition')} {product.get('sku')}"
            )

            for tag in woocommerce_tag_parser_model.tags:
                woocommerce_tag_model = self.woocommerce_service_provider.woocommerce_tag_model()
                woocommerce_tag_model.name = tag
                woocommerce_tags_model.append(woocommerce_tag_model)

            self.ziel_woocommerce_product_model.meta_data = self.rank_math_model.for_use_in_woocommerce()
            self.ziel_woocommerce_product_model.name = ki_dict.get("title")
            self.ziel_woocommerce_product_model.description = ki_dict.get("description")
            self.ziel_woocommerce_product_model.short_description = ki_dict.get("short_description")

            self.ziel_woocommerce_product_model.slug = ""
            self.ziel_woocommerce_product_model.permalink = ""
            self.ziel_woocommerce_product_model.catalog_visibility = "visible"
            self.ziel_woocommerce_product_model.sku = ""
            self.ziel_woocommerce_product_model.price = Numbers.price_anpassen(product.get("price")["value"], price_anpassen)
            self.ziel_woocommerce_product_model.regular_price = Numbers.price_anpassen(product.get("price")["value"], price_anpassen)
            self.ziel_woocommerce_product_model.sale_price = Numbers.price_anpassen(product.get("price")["value"], (price_anpassen - 0.1))
            self.ziel_woocommerce_product_model.on_sale = True
            self.ziel_woocommerce_product_model.tax_status = "taxable"
            self.ziel_woocommerce_product_model.tax_class = ""
            self.ziel_woocommerce_product_model.manage_stock = False
            self.ziel_woocommerce_product_model.shipping_required = True
            self.ziel_woocommerce_product_model.shipping_taxable = True
            self.ziel_woocommerce_product_model.shipping_class = ""
            self.ziel_woocommerce_product_model.shipping_class_id = 0
            self.ziel_woocommerce_product_model.stock_status = "instock"
            self.ziel_woocommerce_product_model.categories = woocommerce_categories_model
            self.ziel_woocommerce_product_model.brands = woocommerce_brands_model
            self.ziel_woocommerce_product_model.tags = woocommerce_tags_model
            self.ziel_woocommerce_product_model.images = woocommerce_images_model
            self.woocommerce_product_models.append(self.ziel_woocommerce_product_model)

            return self.woocommerce_product_models

    # --
    # ...
    # --

    def upload_product_model_to_woocommerce(self, target_woocommerce_category_name: str) -> bool:
        target_woocommerce_category_model = self.woocommerce_service_provider.woocommerce_category_model(
            name=target_woocommerce_category_name
        )

        for product_model in self.woocommerce_product_models:
            product_model.categories = [target_woocommerce_category_model]
            self.woocommerce_service_provider.woocommerce_uploader.resolve_or_upload(product_model=product_model)

            self.waiting(1000)

        self.woocommerce_service_provider.woocommerce_rollback.rollback()
        return True
