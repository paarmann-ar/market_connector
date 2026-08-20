from typing import TYPE_CHECKING

from apis.woocommerce_api.config.woocommerce_api_config import (
    WoocommerceApiConfig,
)
from apis.woocommerce_api.core.base_woocommerce_api import (
    BaseWoocommerceApi,
)
from ki.prompt_provider.models.input_message_model import InputMessageModel
from toolboxs.html import Html

if TYPE_CHECKING:
    from apis.ebay_api.models.browse.product_ebay_model import ProductEbayModel

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
            "buying",
            "purchase",
            "purchasing",
            "ordering",
            "order",
            "offer",
            "listing",
            "sale",
            "selling",
            "selling conditions",
            "payment",
            "payment received",
            "payment terms",
            "price",
            "pricing",
            "invoice",
            "billing",
            "VAT",
            "tax",
            "taxes",
            "Mehrwertsteuer",
            "MwSt.",
            "Steuer",
            "Rechnungen",
            "Zahlung",
            "Zahlungsbedingungen",
            "Versand",
            "Versandkosten",
            "Versand nach Zahlung",
            "shipping",
            "delivery",
            "delivery time",
            "Lieferzeit",
            "Lieferadresse",
            "shipping address",
            "buyer",
            "customer",
            "purchaser",
            "Käufer",
            "Kunde",
            "purchase before",
            "before buying",
            "nach dem Kauf",
            "vor dem Kauf",
            "after purchase",
            "contact before purchase",
            "contact before buying",
            "return",
            "refund",
            "Rückgabe",
            "Rücksendung",
            "Erstattung",
            "warranty",
            "Garantie",
            "liability",
            "responsibility",
            "buyer responsibility",
            "customs",
            "customs duties",
            "import duties",
            "Zölle",
            "Zoll",
            "Einfuhrzölle",
            "Verpackung",
            "package",
            "parcel",
            "Versandkarton",
            "Füllmaterial",
            "shipping box",
            "shipping protection",
            "contact information",
            "Kontakt",
            "email",
            "E-Mail",
            "phone",
            "Telefon",
            "website",
            "Homepage",
            "support",
            "service",
            "contact us",
            "melden",
            "Lösung",
            "Reklamation",
            "Über uns",
            "About us",
            "Company introduction",
            "Company history",
            "Contact information",
            "Address",
            "Phone number",
            "Email address",
            "Website information",
            "Shipping information",
            "Payment information",
            "Return policy",
            "Warranty information",
            "Legal notices",
            "General company slogans",
            "Marketing texts unrelated to the product",
            "More auctions in our shop",
            "Other generic company information",
            "Zölle",
            "Zoll",
            "Zollgebühren",
            "Einfuhrzölle",
            "Importzölle",
            "Steuern",
            "Mehrwertsteuer",
            "MwSt.",
            "VAT",
            "TVA",
            "Taxes",
            "Customs duties",
            "Customs fees",
            "Import fees",
            "Versandkosten",
            "Versand",
            "Shipping",
            "Delivery",
            "Lieferkosten",
            "Käufer trägt die Kosten",
            "Kosten trägt der Käufer",
            "buyer is responsible",
            "buyer's responsibility",
            "payment",
            "Zahlung",
            "Zahlungsbedingungen",
            "Rückgabe",
            "Retour",
            "Rücksendung",
            "Return",
            "Refund",
            "Erstattung",
            "Warranty",
            "Garantie",
            "Rechnung",
        ]

        for section in remove_sections:
            index = text.find(section)
            if index != -1:
                text = text[:index]

        return text.strip()

    # --
    # ...
    # --

    def use_ki_to_rewrite_metadata_to_woocommerce(self, product_ebay_model: "ProductEbayModel") -> dict:

        try:
            item_id = product_ebay_model.itemId
            title = product_ebay_model.title
            description = self.clean_product_description(text=product_ebay_model.description)
            description = Html.remove_html_tags(context=description)[:1500]
            short_description = Html.remove_html_tags(context=product_ebay_model.shortDescription)[:500]

            brand = product_ebay_model.brand
            condition = product_ebay_model.condition
            mpn = product_ebay_model.mpn

            input_message_model = InputMessageModel()
            input_message_model.md_file_name = "product_content"

            input_message_model.inputs = {
                "cache_id": item_id,
                "title": title,
                "description": description,
                "short_description": short_description,
                "brand": brand,
                "condition": condition,
                "mpn": mpn,
            }

            ki_message = self.ollama.get_seo_from_ollama_generate_for_rankmath(input_message_model=input_message_model)

            self.rank_math_model.clear()
            self.rank_math_model.rank_math_title = ki_message.get("title")
            self.rank_math_model.rank_math_description = ki_message.get("meta_description")
            focus_keywords = ki_message.get("focus_keywords")

            if isinstance(focus_keywords, list):
                focus_keywords = ", ".join(focus_keywords)

            self.rank_math_model.rank_math_focus_keyword = f"{focus_keywords}, {brand}"

            self.prompt_on_screen(f"use_ki_to_rewrite_metadata_to_woocommerce: {ki_message}")

            return ki_message

        except Exception as exp:
            self.error(f"use_ki_to_rewrite_metadata_to_woocommerce: {exp}")
