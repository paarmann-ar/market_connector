from apis.woocommerce_api.config.woocommerce_api_config import (
    WoocommerceApiConfig,
)
from apis.woocommerce_api.core.base_woocommerce_api import (
    BaseWoocommerceApi,
)
from ki.prompt_provider.models.input_message_model import InputMessageModel
from toolboxs.html import Html

# --
# ...
# --


class CreateProductSeo(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(self):
        return WoocommerceApiConfig().get_dictionary()

    # --
    # ...
    # --

    def clean_product_description(self, text: str) -> str:

        remove_sections = [
            "BEZAHLUNG",
            "VERSAND",
            "Zahlung & Versand",
            "Über uns",
            "Kompatibilität",
            "Viele weitere Angebote",
            "Fahrzeugverwendungsliste",
            "OE-Vergleichsnummern",
            "PASSEND DAZU",
            "Kontaktieren Sie uns",
            "Design & Development",
            "Rücknahmen",
        ]

        for section in remove_sections:
            index = text.find(section)
            if index != -1:
                text = text[:index]

        return text.strip()

    # --
    # ...
    # --

    def use_ki_to_rewrite_metadata_to_woocommerce(self, product: dict) -> dict:

        try:
            title = product.get("title")
            description = self.clean_product_description(text=product.get("description", ""))
            description = Html.remove_html_tags(context=description)[:1500]
            short_description = Html.remove_html_tags(context=product.get("short_description", ""))[:500]

            brand = product.get("brand", "")
            condition = product.get("condition")
            sku = product.get("sku")

            input_message_model = InputMessageModel()
            input_message_model.md_file_name = "product_content"

            input_message_model.inputs = {
                "title": title,
                "description": description,
                "short_description": short_description,
                "brand": brand,
                "condition": condition,
                "sku": sku,
            }

            ki_message = self.ollama.get_seo_from_ollama_generate_for_rankmath(input_message_model=input_message_model)

            self.rank_math_model.clear()
            self.rank_math_model.rank_math_title = product.get("title")
            self.rank_math_model.rank_math_description = product.get("meta_description")
            focus_keywords = ki_message.get("focus_keywords")

            if isinstance(focus_keywords, list):
                focus_keywords = ", ".join(focus_keywords)

            self.rank_math_model.rank_math_focus_keyword = focus_keywords

            self.prompt_on_screen(f"use_ki_to_rewrite_metadata_to_woocommerce: {ki_message}")

            return ki_message

        except Exception as exp:
            self.error(f"use_ki_to_rewrite_metadata_to_woocommerce: {exp}")
