import json
from dataclasses import asdict, dataclass
from typing import Optional

# --
# ...
# --


@dataclass
class SearchInEbayModel:
    category_name_candidate: Optional[str] = None
    conditions: Optional[str] = None
    deliveryCountry: Optional[str] = None
    q: Optional[str] = None

    # --
    # ...
    # --

    def to_json(self):
        return json.dumps(asdict(self), ensure_ascii=False)

    # --
    # ...
    # --

    def to_dict(self):
        data = asdict(self)
        self.filter_product = f"conditions:{self.conditions},deliveryCountry:{self.deliveryCountry}"
        data["filter_product"] = self.filter_product
        return data

    # --
    # ...
    # --

    def get_all_attributes(self):
        return asdict(self)
