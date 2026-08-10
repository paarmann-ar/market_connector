import json
from dataclasses import asdict, dataclass
from typing import Optional

# --
# ...
# --


@dataclass
class WoocommerceBrandModel:
    id: Optional[int] = None
    name: Optional[str] = "No Brand"
    slug: Optional[str] = None
    description: Optional[str] = None

    # --
    # ...
    # --

    def to_json(self):
        return json.dumps(asdict(self), ensure_ascii=False)

    # --
    # ...
    # --

    def to_dict(self):
        return asdict(self)

    # --
    # ...
    # --

    @classmethod
    def from_api(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            slug=data["slug"],
            description=data["description"],
        )
