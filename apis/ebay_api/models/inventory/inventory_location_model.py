import json
from dataclasses import asdict, dataclass, fields
from typing import Any, Optional


# --
# ...
# --
@dataclass
class InventoryLocationModel:
    merchant_location_key: Optional[str] = "My Warehouse"
    location: Optional[Any] = None
    locationTypes: Optional[Any] = None

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

    def to_payload(self) -> dict:
        return {
            "location": self.location,
            "locationTypes": self.locationTypes,
        }
