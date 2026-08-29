import json
from dataclasses import asdict, dataclass, fields, field
from typing import Any, Optional

# --
# ...
# --


@dataclass
class ZalandoLoungeSimpleModel:
    country_sizes: dict[str, str] = field(default_factory=dict)

    supplier_size: Optional[str] = None
    supplier_size_country: Optional[str] = None

    delivery_promise: Optional[dict[str, Any]] = None

    shipping_fee: Optional[dict[str, Any]] = None

    filterName: Optional[str] = None
    filterValue: Optional[str] = None

    price: Optional[int] = None
    specialPrice: Optional[int] = None

    sku: Optional[str] = None

    stockStatus: Optional[str] = None
    stockHasReservations: bool = False

    gtin: Optional[str] = None

    # --
    # ...
    # --

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    # --
    # ...
    # --

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            ensure_ascii=False,
        )

    # --
    # ...
    # --

    @classmethod
    def from_api(
        cls,
        data: dict[str, Any],
    ) -> "ZalandoLoungeSimpleModel":

        return cls(
            country_sizes=data.get(
                "country_sizes",
                {},
            ),
            supplier_size=data.get("supplier_size"),
            supplier_size_country=data.get("supplier_size_country"),
            delivery_promise=data.get("delivery_promise"),
            shipping_fee=data.get("shipping_fee"),
            filterName=data.get("filterName"),
            filterValue=data.get("filterValue"),
            price=data.get("price"),
            specialPrice=data.get("specialPrice"),
            sku=data.get("sku"),
            stockStatus=data.get("stockStatus"),
            stockHasReservations=data.get(
                "stockHasReservations",
                False,
            ),
            gtin=data.get("gtin"),
        )
