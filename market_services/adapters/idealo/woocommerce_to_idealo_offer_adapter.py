from apis.idealo_api.models.idealo_offer_model import IdealoOfferModel
from apis.woocommerce_api.models.woocommerce_product_model import (
    WoocommerceProductModel,
)


class WoocommerceToIdealoOfferAdapter:

    @classmethod
    def from_woocommerce(
        cls,
        woocommerce_product_model: WoocommerceProductModel,
        *,
        delivery: str | None = None,
        delivery_costs: dict[str, str] | None = None,
        payment_costs: dict[str, str] | None = None,
        free_return_days: int | None = None,
    ) -> IdealoOfferModel:

        meta_data = woocommerce_product_model.meta_data

        is_used = cls.normalize_condition_bool(meta_data)

        return IdealoOfferModel(
            sku=woocommerce_product_model.sku,
            title=woocommerce_product_model.name,
            price=cls.normalize_price(woocommerce_product_model.sale_price),
            former_price=cls.normalize_price(
                woocommerce_product_model.regular_price
            ),
            url=woocommerce_product_model.permalink,
            brand=cls.get_brand(woocommerce_product_model),
            category_path=cls.get_category_path(woocommerce_product_model),
            description=(
                woocommerce_product_model.short_description
                or woocommerce_product_model.description
            ),
            image_urls=cls.get_image_urls(woocommerce_product_model),
            delivery=delivery,
            delivery_costs=delivery_costs,
            payment_costs=payment_costs,
            free_return_days=free_return_days,

            used=is_used,
            condition=None if is_used else cls.normalize_condition(meta_data),
            condition_type=None if is_used else cls.normalize_condition_type(meta_data),

            replica=False,
            download=False,
        )

    @staticmethod
    def normalize_price(value: str | None) -> str | None:
        if not value:
            return None

        return f"{float(value):.2f}"

    @classmethod
    def normalize_condition(
        cls,
        meta_data: list[dict] | None,
    ) -> str | None:
        if not meta_data:
            return None

        for item in meta_data:
            if item.get("key") == "condition_value":
                return item.get("value")

        return None

    @classmethod
    def normalize_condition_type(
        cls,
        meta_data: list[dict] | None,
    ) -> str | None:
        if not meta_data:
            return None

        for item in meta_data:
            if item.get("key") == "condition":
                return item.get("value")

        return None

    @classmethod
    def normalize_condition_bool(
        cls,
        meta_data: list[dict] | None,
    ) -> bool:
        if not meta_data:
            return False

        for item in meta_data:
            if item.get("key") == "condition":
                return str(item.get("value", "")).upper() == "USED"

        return False

    @staticmethod
    def get_brand(
        woocommerce_product_model: WoocommerceProductModel,
    ) -> str | None:
        if not woocommerce_product_model.brands:
            return None

        return woocommerce_product_model.brands[0].name or None

    @staticmethod
    def get_category_path(
        woocommerce_product_model: WoocommerceProductModel,
    ) -> list[str]:
        return [
            category.name
            for category in woocommerce_product_model.categories
            if category.name
        ]

    @staticmethod
    def get_image_urls(
        woocommerce_product_model: WoocommerceProductModel,
    ) -> list[str]:
        return [
            image.src
            for image in woocommerce_product_model.images
            if getattr(image, "src", None)
        ]