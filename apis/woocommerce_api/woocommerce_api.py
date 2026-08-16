from typing import TYPE_CHECKING

from apis.woocommerce_api.config.woocommerce_api_config import (
    WoocommerceApiConfig,
)
from apis.woocommerce_api.core.base_woocommerce_api import (
    BaseWoocommerceApi,
)
from apis.woocommerce_api.create_product_seo import CreateProductSeo
from apis.woocommerce_api.models.woocommerce_product_model import WoocommerceProductModel
from toolboxs.numbers import Numbers
from toolboxs.text import Text

if TYPE_CHECKING:
    from apis.ebay_api.models.product_ebay_model import ProductEbayModel

# --
# ...
# --


class WoocommerceApi(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

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
        self, product_ebay_models: list["ProductEbayModel"]
    ) -> list[WoocommerceProductModel]:
        woocommerce_product_models: list[WoocommerceProductModel] = []

        for product_ebay_model in product_ebay_models:
            woocommerce_categories_model: list = []
            woocommerce_brands_model: list = []
            woocommerce_tags_model: list = []
            woocommerce_images_model: list = []

            ki_dict = self.create_product_seo.use_ki_to_rewrite_metadata_to_woocommerce(product_ebay_model=product_ebay_model)

            alt_image_constructor = " ".join(ki_dict.get("focus_keywords", ["_", "_"]))
            image_alt = Text().remove_dublicate_words_from_string(alt_image_constructor)
            image_alt_main = ki_dict.get("title").split("|")[0]

            ziel_woocommerce_product_model = self.woocommerce_service_provider.woocommerce_product_model()

            woocommerce_images_model.insert(
                0,
                self.woocommerce_service_provider.woocommerce_image_model.from_api(
                    {"src": product_ebay_model.image["imageUrl"], "alt": image_alt_main, "is_main_image": True}
                ),
            )
            for image_url in product_ebay_model.additionalImages:
                woocommerce_images_model.append(
                    self.woocommerce_service_provider.woocommerce_image_model.from_api({"src": image_url.get("imageUrl"), "alt": image_alt})
                )

            # chon faghat akharin category mikhastam dashteh basham
            category = product_ebay_model.categoryPath.split("|")[-1]
            woocommerce_categories_model.append(self.woocommerce_service_provider.woocommerce_category_model(name=category))

            woocommerce_brands_model.append(self.woocommerce_service_provider.woocommerce_brand_model(name=product_ebay_model.brand))

            woocommerce_tag_parser_model = self.woocommerce_service_provider.woocommerce_tag_parser.woocommerce_tag_parser(
                context=f"{product_ebay_model.title} {product_ebay_model.brand} {product_ebay_model.condition}"
            )

            for tag in woocommerce_tag_parser_model.tags:
                woocommerce_tag_model = self.woocommerce_service_provider.woocommerce_tag_model()
                woocommerce_tag_model.name = tag
                woocommerce_tags_model.append(woocommerce_tag_model)

            ziel_woocommerce_product_model.meta_data = self.rank_math_model.for_use_in_woocommerce()
            ziel_woocommerce_product_model.name = ki_dict.get("title")
            ziel_woocommerce_product_model.description = ki_dict.get("description")
            ziel_woocommerce_product_model.short_description = ki_dict.get("short_description")

            ziel_woocommerce_product_model.slug = ""
            ziel_woocommerce_product_model.permalink = ""
            ziel_woocommerce_product_model.catalog_visibility = "visible"
            ziel_woocommerce_product_model.sku = ""
            ziel_woocommerce_product_model.price = Numbers.price_anpassen(
                product_ebay_model.price["value"], product_ebay_model.price_anpassen
            )
            ziel_woocommerce_product_model.regular_price = Numbers.price_anpassen(
                product_ebay_model.price["value"], product_ebay_model.price_anpassen
            )
            ziel_woocommerce_product_model.sale_price = Numbers.price_anpassen(
                product_ebay_model.price["value"], (product_ebay_model.price_anpassen - 0.1)
            )
            ziel_woocommerce_product_model.on_sale = True
            ziel_woocommerce_product_model.tax_status = "taxable"
            ziel_woocommerce_product_model.tax_class = ""
            ziel_woocommerce_product_model.manage_stock = False
            ziel_woocommerce_product_model.shipping_required = True
            ziel_woocommerce_product_model.shipping_taxable = True
            ziel_woocommerce_product_model.shipping_class = ""
            ziel_woocommerce_product_model.shipping_class_id = 0
            ziel_woocommerce_product_model.stock_status = "instock"
            ziel_woocommerce_product_model.categories = woocommerce_categories_model
            ziel_woocommerce_product_model.brands = woocommerce_brands_model
            ziel_woocommerce_product_model.tags = woocommerce_tags_model
            ziel_woocommerce_product_model.images = woocommerce_images_model
            woocommerce_product_models.append(ziel_woocommerce_product_model)

        return woocommerce_product_models

    # --
    # ...
    # --

    def upload_product_model_to_woocommerce(
        self, woocommerce_product_models: list[WoocommerceProductModel], target_woocommerce_category_name: str
    ) -> bool:
        target_woocommerce_category_model = self.woocommerce_service_provider.woocommerce_category_model(
            name=target_woocommerce_category_name
        )

        for woocommerce_product_model in woocommerce_product_models:
            woocommerce_product_model.categories = [target_woocommerce_category_model]

            self.woocommerce_service_provider.woocommerce_uploader.resolve_or_upload(woocommerce_product_model=woocommerce_product_model)

            self.waiting(1000)

        self.woocommerce_service_provider.woocommerce_rollback.rollback()
        return True
