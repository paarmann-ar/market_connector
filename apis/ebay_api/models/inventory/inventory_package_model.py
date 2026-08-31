from dataclasses import dataclass
from typing import Any, Optional

# --
# ...
# --


@dataclass
class InventoryWeightModel:
    value: Optional[float] = None
    unit: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {}

        if self.value is not None:
            data["value"] = self.value

        if self.unit is not None:
            data["unit"] = self.unit

        return data


# --
# ...
# --


@dataclass
class InventoryDimensionModel:
    length: Optional[float] = None
    width: Optional[float] = None
    height: Optional[float] = None
    unit: Optional[str] = None

    #  --
    #  ...
    #  --

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {}

        if self.length is not None:
            data["length"] = self.length

        if self.width is not None:
            data["width"] = self.width

        if self.height is not None:
            data["height"] = self.height

        if self.unit is not None:
            data["unit"] = self.unit

        return data


# --
# ...
# --


@dataclass
class InventoryPackageWeightAndSizeModel:
    packageType: Optional[str] = None
    shippingIrregular: Optional[bool] = None

    weight: Optional[InventoryWeightModel] = None
    dimensions: Optional[InventoryDimensionModel] = None

    #  --
    #  ...
    #  --

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {}

        if self.packageType is not None:
            data["packageType"] = self.packageType

        if self.shippingIrregular is not None:
            data["shippingIrregular"] = self.shippingIrregular

        if self.weight is not None:
            data["weight"] = self.weight.to_dict()

        if self.dimensions is not None:
            data["dimensions"] = self.dimensions.to_dict()

        return data
