from apis.woocommerce_api.config.woocommerce_api_config import (
    WoocommerceApiConfig,
)
from apis.woocommerce_api.core.base_woocommerce_api import (
    BaseWoocommerceApi,
)
from ki.prompt_provider.models.input_message_model import InputMessageModel

# --
# ...
# --


class WoocommerceApi(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.woocommerce_product_models: list = []
        self.ziel_woocommerce_product_model = (
            self.woocommerce_service_provider.woocommerce_product_model()
        )

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

    def use_ki_to_add_seo_with_rankmath_to_woocommerce(self, product: dict) -> bool:

        try:
            self.rank_math_model.clear()

            input_message_model = InputMessageModel()
            input_message_model.md_file_name = "seo"
            input_message_model.inputs = {
                "title": product.get("title"),
                "description": product.get("description"),
            }

            ki_message = self.ollama.get_seo_from_ollama_generate_for_rankmath(
                input_message_model=input_message_model
            )

            self.rank_math_model.rank_math_title = ki_message["title"]
            self.rank_math_model.rank_math_description = ki_message["meta_description"]
            self.rank_math_model.rank_math_focus_keyword = ki_message["focus_keywords"]

            return self.rank_math_model.for_use_in_woocommerce()

        except Exception as exp:
            self.error(f"use_ki_to_add_seo_with_rankmath_to_woocommerce: {exp}")

    # --
    # ...
    # --

    def use_ki_to_rewrite_title_and_description_to_woocommerce(
        self, product: dict
    ) -> bool:

        try:
            input_message_model = InputMessageModel()
            input_message_model.md_file_name = "product_description"

            input_message_model.inputs = {
                "title": product.get("title"),
                "description": product.get("description"),
                "short_description": product.get("shortDescription"),
            }

            ki_message = self.ollama.get_seo_from_ollama_generate_for_rankmath(
                input_message_model=input_message_model
            )

            self.ziel_woocommerce_product_model.name = ki_message["title"]
            self.ziel_woocommerce_product_model.description = ki_message["description"]
            self.ziel_woocommerce_product_model.short_description = ki_message[
                "short_description"
            ]

            return True

        except Exception as exp:
            self.error(f"use_ki_to_rewrite_title_and_description_to_woocommerce: {exp}")

    # --
    # ...
    # --

    def convert_ebay_product_model_to_woocommerce_product_model(
        self, ebay_product_detail_model_list: object, price_anpassen: float
    ) -> None:
        for product in ebay_product_detail_model_list:
            woocommerce_categories_model: list = []
            woocommerce_brands_model: list = []
            woocommerce_tags_model: list = []
            woocommerce_images_model: list = []
            woocommerce_seos_model: list = []

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
                self.woocommerce_service_provider.woocommerce_category_model(
                    name=category
                )
            )

            woocommerce_brands_model.append(
                self.woocommerce_service_provider.woocommerce_brand_model(
                    name=product.get("brand")
                )
            )

            woocommerce_tag_parser_model = self.woocommerce_service_provider.woocommerce_tag_parser.woocommerce_tag_parser(
                context=f"{product['title']} {product.get('brand')} {product.get('condition')} {product.get('sku')}"
            )

            for tag in woocommerce_tag_parser_model.tags:
                woocommerce_tag_model = (
                    self.woocommerce_service_provider.woocommerce_tag_model()
                )
                woocommerce_tag_model.name = tag
                woocommerce_tags_model.append(woocommerce_tag_model)

            woocommerce_seos_model = (
                self.use_ki_to_add_seo_with_rankmath_to_woocommerce(product=product)
            )

            self.use_ki_to_rewrite_title_and_description_to_woocommerce(product=product)

            self.ziel_woocommerce_product_model.slug = ""
            self.ziel_woocommerce_product_model.permalink = ""
            self.ziel_woocommerce_product_model.catalog_visibility = "visible"
            # description=BeautifulSoup(
            #     product.get("description", ""), "html.parser"
            # ).get_text(separator=" ", strip=True),
            # short_description=BeautifulSoup(
            #     product.get("shortDescription", ""), "html.parser"
            # ).get_text(separator=" ", strip=True),
            self.ziel_woocommerce_product_model.sku = ""
            self.ziel_woocommerce_product_model.price = str(
                round(float(product["price"]["value"]) * price_anpassen)
            )
            self.ziel_woocommerce_product_model.regular_price = str(
                round(float(product["price"]["value"]) * price_anpassen)
            )
            self.ziel_woocommerce_product_model.sale_price = str(
                round(float(product["price"]["value"]) * (price_anpassen - 0.1))
            )
            self.ziel_woocommerce_product_model.on_sale = True
            self.ziel_woocommerce_product_model.tax_status = "taxable"
            self.ziel_woocommerce_product_model.tax_class = ""
            self.ziel_woocommerce_product_model.manage_stock = False
            self.ziel_woocommerce_product_model.shipping_required = True
            self.ziel_woocommerce_product_model.shipping_taxable = True
            self.ziel_woocommerce_product_model.shipping_class = ""
            self.ziel_woocommerce_product_model.shipping_class_id = 0
            self.ziel_woocommerce_product_model.stock_status = "instock"
            self.ziel_woocommerce_product_model.categories = (
                woocommerce_categories_model
            )
            self.ziel_woocommerce_product_model.brands = woocommerce_brands_model
            self.ziel_woocommerce_product_model.tags = woocommerce_tags_model
            self.ziel_woocommerce_product_model.images = woocommerce_images_model
            self.ziel_woocommerce_product_model.meta_data = woocommerce_seos_model

            self.woocommerce_product_models.append(self.ziel_woocommerce_product_model)

    # --
    # ...
    # --

    def upload_product_model_to_woocommerce(
        self, target_woocommerce_category_name: str
    ) -> bool:
        target_woocommerce_category_model = (
            self.woocommerce_service_provider.woocommerce_category_model(
                name=target_woocommerce_category_name
            )
        )

        for product_model in self.woocommerce_product_models:
            product_model.categories = [target_woocommerce_category_model]
            self.woocommerce_service_provider.woocommerce_uploader.resolve_or_upload(
                product_model=product_model
            )

            self.waiting(1000)

        self.woocommerce_service_provider.woocommerce_rollback.rollback()
        return True
