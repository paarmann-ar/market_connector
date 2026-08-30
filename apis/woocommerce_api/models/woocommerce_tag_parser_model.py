import json
from dataclasses import asdict, dataclass
from typing import Optional
from pydantic import BaseModel

# --
# ...
# --


class WoocommerceTagParserModel(BaseModel):
    name: str = ""
    brand: Optional[str] = None
    condition: Optional[str] = None
    part_number: Optional[str] = None
    tags: list[str] = None
    category: Optional[str] = None

    # --
    # ...
    # --

    def to_dict(self):
        return self.model_dump()

    # --
    # ...
    # --

    def to_json(self):
        return self.model_dump_json()
