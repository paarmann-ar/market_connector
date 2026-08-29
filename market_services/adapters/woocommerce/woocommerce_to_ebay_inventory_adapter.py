from typing import Optional

from apis.ebay_api.models.inventory.inventory_product_details_model import (
    InventoryProductDetailsModel,
)
from apis.ebay_api.models.inventory.inventory_product_model import (
    InventoryProductModel,
)
from apis.woocommerce_api.models.woocommerce_product_model import (
    WoocommerceProductModel,
)


class WoocommerceToEbayInventoryAdapter:
    def __init__(
        self,
        woocommerce_product: WoocommerceProductModel,
        price_anpassen: float = 1.60,
    ):
        self.woocommerce_product = woocommerce_product
        self.price_anpassen = price_anpassen

    # --------------------------------------------------
    # Main adapter
    # --------------------------------------------------

    def adapt(self) -> InventoryProductModel:

        product = self.woocommerce_product

        return InventoryProductModel(
            sku=product.sku,
            product=self._adapt_product_details(),
            condition="NEW",
            quantity=self._adapt_quantity(),
            price=self._adapt_price(),
        )

    # --------------------------------------------------
    # Product details
    # --------------------------------------------------

    def _adapt_product_details(self) -> InventoryProductDetailsModel:

        product = self.woocommerce_product

        return InventoryProductDetailsModel(
            title=product.name,
            description=product.description,
            imageUrls=self._adapt_images(),
            brand=self._adapt_brand(),
            mpn=self._adapt_mpn(),
            gtin=self._adapt_gtin(),
            aspects=self._adapt_aspects(),
        )

    # --------------------------------------------------
    # Images
    # --------------------------------------------------

    def _adapt_images(self) -> list[str]:

        images = self.woocommerce_product.images

        if not images:
            return []

        result = []

        for image in images:
            if isinstance(image, dict):
                src = image.get("src")
            else:
                src = image.src

            if src:
                result.append(src)

        return result

    # --------------------------------------------------
    # Brand
    # --------------------------------------------------

    def _adapt_brand(self) -> Optional[str]:

        brands = self.woocommerce_product.brands

        if not brands:
            return None

        brand = brands[0]

        if isinstance(brand, dict):
            return brand.get("name")

        return brand.name

    # --------------------------------------------------
    # MPN
    # --------------------------------------------------

    def _adapt_mpn(self) -> Optional[str]:

        return self._get_attribute_value("MPN")

    # --------------------------------------------------
    # GTIN
    # --------------------------------------------------

    def _adapt_gtin(self) -> Optional[str]:

        for name in [
            "GTIN",
            "EAN",
            "UPC",
            "ISBN",
        ]:
            value = self._get_attribute_value(name)

            if value:
                return value

        return None

    # --------------------------------------------------
    # Quantity
    # --------------------------------------------------

    def _adapt_quantity(self) -> int:

        product = self.woocommerce_product

        if product.stock_status != "instock":
            return 0

        return 1

    # --------------------------------------------------
    # Price
    # --------------------------------------------------

    def _adapt_price(self) -> Optional[str]:

        price = self.woocommerce_product.price

        if not price:
            return None

        try:
            price = float(price)

            price *= self.price_anpassen

            return f"{price:.2f}"

        except (TypeError, ValueError):
            return None

    # --------------------------------------------------
    # Attributes -> eBay Aspects
    # --------------------------------------------------

    def _adapt_aspects(self) -> dict[str, list[str]]:

        attributes = self.woocommerce_product.attributes

        if not attributes:
            return {}

        aspects = {}

        for attribute in attributes:
            if isinstance(attribute, dict):
                name = attribute.get("name")
                options = attribute.get("options", [])

            else:
                name = getattr(attribute, "name", None)
                options = getattr(attribute, "options", [])

            if not name or not options:
                continue

            if not isinstance(options, list):
                options = [options]

            aspects[name] = [str(option) for option in options if option is not None]

        return aspects

    # --------------------------------------------------
    # Attribute helper
    # --------------------------------------------------

    def _get_attribute_value(
        self,
        attribute_name: str,
    ) -> Optional[str]:

        attributes = self.woocommerce_product.attributes

        if not attributes:
            return None

        target = attribute_name.strip().lower()

        for attribute in attributes:
            if isinstance(attribute, dict):
                name = attribute.get("name")
                options = attribute.get("options", [])

            else:
                name = getattr(attribute, "name", None)
                options = getattr(attribute, "options", [])

            if not name:
                continue

            if name.strip().lower() != target:
                continue

            if not options:
                return None

            if isinstance(options, list):
                return str(options[0])

            return str(options)

        return None
