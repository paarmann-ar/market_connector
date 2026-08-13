import json
from dataclasses import asdict, dataclass
from typing import Optional

# --
# ...
# --


@dataclass
class SearchInEbayModel:
    category_name_candidate: Optional[str] = None
    category_id = Optional[int]
    product_id = Optional[int]
    marketplace: Optional[str] = "EBAY_DE"
    marketplace_id: Optional[str] = "EBAY_DE"
    deliveryCountry: Optional[str] = "DE"
    conditions: Optional[str] = "{NEW|USED}"
    filter: Optional[str] = None
    q: Optional[str] = None
    total: Optional[int] = None
    item_to_fetch: Optional[int] = 1000
    price_anpassen: Optional[int] = 1.60
    target_category_name_in_woocommerce: Optional[str] = "Sensoren"

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
        return data

    # --
    # ...
    # --

    def generate_filter(self):
        self.filter = f"conditions:{self.conditions},deliveryCountry:{self.deliveryCountry},{self.filter}"

    # --
    # ...
    # --

    def get_all_attributes(self):
        return asdict(self)
