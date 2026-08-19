import json
from dataclasses import dataclass, fields
from typing import Any, Optional

from apis.ebay_api.models.inventory.inventory_availability_model import (
    InventoryAvailabilityModel,
)

from apis.ebay_api.models.inventory.inventory_condition_descriptor_model import (
    InventoryConditionDescriptorModel,
)

from apis.ebay_api.models.inventory.inventory_package_model import (
    InventoryPackageWeightAndSizeModel,
)

from apis.ebay_api.models.inventory.inventory_product_details_model import (
    InventoryProductDetailsModel,
)

# --
# ...
# --


@dataclass
class InventoryProductModel:
    sku: Optional[str] = None

    product: Optional[InventoryProductDetailsModel] = None

    availability: Optional[InventoryAvailabilityModel] = None

    condition: Optional[str] = None
    quantity: Optional[int] = 1
    price: Optional[str] = None
    conditionDescription: Optional[str] = None

    conditionDescriptors: Optional[list[InventoryConditionDescriptorModel]] = None

    packageWeightAndSize: Optional[InventoryPackageWeightAndSizeModel] = None

    # --
    # ...
    # --

    def __init__(self, **kwargs):

        valid_fields = {field.name for field in fields(self)}

        for key, value in kwargs.items():
            # Ignore unknown fields
            if key not in valid_fields:
                continue

            setattr(self, key, value)

    # --
    # ...
    # --

    def to_dict(self) -> dict[str, Any]:

        data: dict[str, Any] = {}

        if self.sku is not None:
            data["sku"] = self.sku

        if self.product is not None:
            data["product"] = self.product.to_dict()

        if self.availability is not None:
            data["availability"] = self.availability.to_dict()

        if self.condition is not None:
            data["condition"] = self.condition

        if self.conditionDescription is not None:
            data["conditionDescription"] = self.conditionDescription

        if self.conditionDescriptors is not None:
            data["conditionDescriptors"] = [descriptor.to_dict() for descriptor in self.conditionDescriptors]

        if self.packageWeightAndSize is not None:
            data["packageWeightAndSize"] = self.packageWeightAndSize.to_dict()

        return data

    # --
    # ...
    # --

    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            ensure_ascii=False,
        )
