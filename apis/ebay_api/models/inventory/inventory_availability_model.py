from dataclasses import dataclass
from typing import Any, Optional

# --
# ...
# --


@dataclass
class ShipToLocationAvailabilityModel:
    quantity: Optional[int] = None

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {}

        if self.quantity is not None:
            data["quantity"] = self.quantity

        return data


# --
# ...
# --


@dataclass
class PickupAtLocationAvailabilityModel:
    merchantLocationKey: Optional[str] = None
    quantity: Optional[int] = None
    fulfillmentTime: Optional[dict[str, Any]] = None

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {}

        if self.merchantLocationKey is not None:
            data["merchantLocationKey"] = self.merchantLocationKey

        if self.quantity is not None:
            data["quantity"] = self.quantity

        if self.fulfillmentTime is not None:
            data["fulfillmentTime"] = self.fulfillmentTime

        return data


# --
# ...
# --


@dataclass
class InventoryAvailabilityModel:
    shipToLocationAvailability: Optional[ShipToLocationAvailabilityModel] = None
    pickupAtLocationAvailability: Optional[list[PickupAtLocationAvailabilityModel]] = None

    #  --
    #  ...
    #  --

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {}

        if self.shipToLocationAvailability is not None:
            data["shipToLocationAvailability"] = self.shipToLocationAvailability.to_dict()

        if self.pickupAtLocationAvailability is not None:
            data["pickupAtLocationAvailability"] = [location.to_dict() for location in self.pickupAtLocationAvailability]

        return data
