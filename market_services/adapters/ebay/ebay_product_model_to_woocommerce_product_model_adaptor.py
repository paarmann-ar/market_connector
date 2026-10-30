from apis.ebay_api.models.browse.product_ebay_model import ProductEbayModel
from apis.woocommerce_api.models.woocommerce_brand_model import WoocommerceBrandModel
from apis.woocommerce_api.models.woocommerce_google_product_model import WoocommerceGoogleProductModel
from market_services.adapters.ebay.technical_table_builder import TechnicalTableBuilder

from apis.woocommerce_api.models.woocommerce_category_model import WoocommerceCategoryModel
from apis.woocommerce_api.models.woocommerce_image_model import WoocommerceImageModel
from apis.woocommerce_api.models.woocommerce_product_model import WoocommerceProductModel
from apis.woocommerce_api.models.woocommerce_tag_model import WoocommerceTagModel
from market_services.adapters.ebay.ebay_product_model_to_product_input_metadata_model import EbayProductModelToProductInputMetadataModel
from market_services.adapters.ebay.ebay_assemble_final import assemble_final
from market_services.meta_data_services.meta_data_services import MetaDataServices
from toolboxs.numbers import Numbers
from toolboxs.random_expertion import RandomExpertion
from typing import Optional
from market_services.core.base import Base
from market_services.config.market_services_config import (
    MarketServicesConfig,
)
from apis.woocommerce_api.models.woocommerce_product_model import ConditionValue, Condition
# --
# ...
# --


EBAY_CONDITION_MAP = {
    "1000": {
        "condition": Condition.NEW,
        "de": "Neu",
    },
    "1500": {
        "condition": Condition.NEW,
        "de": "Neu mit Mängeln",
    },
    "2000": {
        "condition": Condition.AS_NEW,
        "de": "Sehr gut",
    },
    "2500": {
        "condition": Condition.REFURBISHED,
        "de": "Generalüberholt",
    },
    "3000": {
        "condition": Condition.USED,
        "de": "Gebraucht",
    },
    "4000": {
        "condition": Condition.USED,
        "de": "Sehr gut",
    },
    "5000": {
        "condition": Condition.USED,
        "de": "Gut",
    },
    "6000": {
        "condition": Condition.USED,
        "de": "Akzeptabel",
    },
}


class EbayProductModelToWoocommerceProductModelAdaptor(Base):
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.prompt_filename = self.config_dictionary.get("ebay_product_model_to_woocommerce_product_model_adaptor_prompt_filename")

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    #  --
    #  ...
    #  --

    @classmethod
    def get_config_dictionary(cls):
        return MarketServicesConfig().get_dictionary()

    #  --
    #  ...
    #  --

    def adapter(self, product_ebay_model: ProductEbayModel) -> WoocommerceProductModel:

        technical_table_builder = TechnicalTableBuilder()
        technical_attributes = technical_table_builder.get_technical_attributes(product_ebay_model=product_ebay_model)

        meta_data_services = MetaDataServices()
        product_output_metadata_model = meta_data_services.create_metadata(
            product_input_metadata_model=EbayProductModelToProductInputMetadataModel().adapter(
                product_ebay_model=product_ebay_model, prompt_filename=self.prompt_filename, technical_attributes=technical_attributes
            ),
            assemble_final=assemble_final,
        )

        woocommerce_tags_model = []
        for tag in product_output_metadata_model.product_tags:
            woocommerce_tag_model = WoocommerceTagModel(name=tag)
            woocommerce_tags_model.append(woocommerce_tag_model)

        woocommerce_images_model: list = []
        image_alt = product_output_metadata_model.image_seo_model.get("image_alt")
        image_alt_main = product_output_metadata_model.image_seo_model.get("image_alt_main")

        woocommerce_images_model.insert(
            0, WoocommerceImageModel().from_api({"src": product_ebay_model.image.imageUrl, "alt": image_alt_main})
        )

        if product_ebay_model.additionalImages:
            for image_url in product_ebay_model.additionalImages:
                woocommerce_images_model.append(WoocommerceImageModel.from_api({"src": image_url.imageUrl, "alt": image_alt}))

        rank_math_metadata = product_output_metadata_model.seo_model
        woocommerce_google_product_model = self._get_google_product(product_ebay_model=product_ebay_model)
        google_metadata = woocommerce_google_product_model.to_meta_data()

        meta_data = [
            *rank_math_metadata,
            *google_metadata,
        ]

        return WoocommerceProductModel(
            categories=self._get_categories(product_ebay_model=product_ebay_model),
            brands=[WoocommerceBrandModel(name=product_ebay_model.brand)],
            tags=woocommerce_tags_model,
            slug=product_output_metadata_model.slug,
            meta_data=meta_data,
            name=product_output_metadata_model.title,
            description=product_output_metadata_model.description,
            short_description=product_output_metadata_model.short_description,
            price=Numbers.price_anpassen(product_ebay_model.price["value"], product_ebay_model.price_anpassen),
            regular_price=Numbers.price_anpassen(product_ebay_model.price["value"], product_ebay_model.price_anpassen),
            sale_price=Numbers.price_anpassen(product_ebay_model.price["value"], (product_ebay_model.price_anpassen - 0.1)),
            images=woocommerce_images_model,
            image_description=product_output_metadata_model.image_description,
            sku=RandomExpertion.sku_generator(),
            on_sale=True,
            manage_stock=True,
            stock_quantity=product_ebay_model.estimatedAvailabilities[0]["estimatedRemainingQuantity"],
            stock_status=self._get_stock_status(product_ebay_model),
            condition= EBAY_CONDITION_MAP.get(product_ebay_model.conditionId, Condition.NEW)["condition"],
            condition_value=ConditionValue.EXCELLENT
        )

    # --
    # ...
    # --

    def _get_categories(
        self,
        product_ebay_model: ProductEbayModel,
    ) -> list[WoocommerceCategoryModel]:

        category_name = product_ebay_model.categoryPath.split("|")[-1]
        category_path = product_ebay_model.categoryPath

        return [WoocommerceCategoryModel(name=category_name, slug=self._slugify(category_name), path=category_path)]

    # --
    # ...
    # --

    @staticmethod
    def _slugify(value: Optional[str]) -> Optional[str]:

        if not value:
            return None

        return value.strip().lower().replace(" ", "-")

    # --
    # ...
    # --

    def _get_stock_status(
        self,
        product_ebay_model: ProductEbayModel,
    ) -> str:

        if (product_ebay_model.estimatedAvailabilities[0]["estimatedRemainingQuantity"] or 0) > 0:
            return "instock"

        return "outofstock"

    # --
    # ...
    # --

    def _get_google_product(self, product_ebay_model: ProductEbayModel) -> WoocommerceGoogleProductModel:

        return WoocommerceGoogleProductModel(
            manufacturer_part_number=product_ebay_model.mpn,
            condition=self._get_google_condition(product_ebay_model),
            gender=self._get_aspect(product_ebay_model, "Gender"),
            size=self._get_aspect(product_ebay_model, "Size"),
            color=self._get_aspect(product_ebay_model, "Color"),
            material=self._get_aspect(product_ebay_model, "Material"),
            pattern=self._get_aspect(product_ebay_model, "Pattern"),
            multipack=product_ebay_model.lotSize,
            adult_content=product_ebay_model.adultOnly,
        )

    # --
    # ...
    # --

    def _get_aspect(self, product_ebay_model: ProductEbayModel, name: str) -> Optional[str]:

        aspects = product_ebay_model.aspects or {}

        for key, values in aspects.items():
            if key.lower() == name.lower() and values:
                return values[0]

        return None

    # --
    # ...
    # --

    def _get_google_condition(self, product_ebay_model: ProductEbayModel) -> Optional[str]:

        condition = (product_ebay_model.condition or "").strip().lower()

        if not condition:
            return None

        if "refurbished" in condition:
            return "refurbished"

        if "used" in condition:
            return "used"

        return "new"
