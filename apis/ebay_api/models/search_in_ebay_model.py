import json
from dataclasses import asdict, dataclass
from typing import Optional

# --
# ...
# --


@dataclass
class SearchInEbayModel:
    category_name_candidate: Optional[str] = None
    conditions: Optional[str] = "{NEW|USED}"
    marketplace: Optional[str] = "EBAY_DE"
    deliveryCountry: Optional[str] = "DE"
    q: Optional[str] = None
    total: Optional[int] = None
    item_to_fetch: Optional[int] = 1000

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
