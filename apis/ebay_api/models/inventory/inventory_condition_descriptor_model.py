from dataclasses import dataclass
from typing import Any, Optional

# --
# ...
# --


@dataclass
class InventoryConditionDescriptorModel:
    name: Optional[str] = None
    values: Optional[list[str]] = None

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {}

        if self.name is not None:
            data["name"] = self.name

        if self.values is not None:
            data["values"] = self.values

        return data
