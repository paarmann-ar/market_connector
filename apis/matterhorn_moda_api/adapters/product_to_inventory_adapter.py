from apis.ebay_api.models.browse.product_ebay_model import (
    ProductEbayModel,
)
from apis.ebay_api.models.inventory import (
    InventoryProductModel,
    InventoryProductDetailsModel,
    InventoryAvailabilityModel,
    ShipToLocationAvailabilityModel,
)

CONDITION_MAP = {
    "New": "NEW",
    "New – Open box": "NEW_OTHER",
    "New: Other (see details)": "NEW_OTHER",
    "Used": "USED",
    "For parts or not working": "FOR_PARTS_OR_NOT_WORKING",
}


class ProductToInventoryAdapter:
    @staticmethod
    def adapt(
        product: ProductEbayModel,
        quantity: int = 1,
    ) -> InventoryProductModel:

        image_urls: list[str] = []

        # Main image
        if product.image and product.image.imageUrl:
            image_urls.append(product.image.imageUrl)

        # Additional images
        if product.additionalImages:
            for image in product.additionalImages:
                if image and image.imageUrl:
                    image_urls.append(image.imageUrl)

        # Remove duplicates while preserving order
        image_urls = list(dict.fromkeys(image_urls))

        if product.condition:
            product.condition = CONDITION_MAP.get(product.condition)

        inventory_product = InventoryProductDetailsModel(
            title=product.title,
            description=product.description,
            imageUrls=image_urls or None,
            brand=product.brand,
            mpn=product.mpn,
            gtin=product.gtin,
            aspects=product.aspects,
        )

        availability = InventoryAvailabilityModel(shipToLocationAvailability=(ShipToLocationAvailabilityModel(quantity=quantity)))

        a = 1
        if product.price["currency"] == "USD":
            a = a * 1.2
            product.price["currency"] = "EUR"
        price = {"value": str(float(product.price["value"]) * product.price_anpassen * a), "currency": product.price["currency"]}

        return InventoryProductModel(
            sku=product.sku,
            product=inventory_product,
            availability=availability,
            condition=product.condition,
            conditionDescription=(product.conditionDescription),
            price=price,
        )
