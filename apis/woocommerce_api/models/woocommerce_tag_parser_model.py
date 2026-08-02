import json
from dataclasses import asdict, dataclass
from typing import Optional

# --
# ...
# --


@dataclass
class WoocommerceTagParserModel:
    name: str = ""
    brand: Optional[str] = None
    condition: Optional[str] = None
    part_number: Optional[str] = None
    tags: list[str] = None
    category: Optional[str] = None

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
