import json
from dataclasses import asdict, dataclass
from typing import Optional
from urllib.parse import urlencode

# --
# ...
# --


@dataclass
class SearchInWoocommerceModel:
    category_name_candidate: Optional[str] = None
    category_id = Optional[int]
    product_id = Optional[int]
    name: Optional[str] = None
    sku: Optional[str] = None
    status: Optional[str] = None
    stock_status: Optional[str] = None
    filter: Optional[str] = None
    item_id: Optional[str] = None
    total: Optional[int] = None
    item_to_fetch: Optional[int] = 5
    price_anpassen: Optional[int] = 1.60
    target_category_name_in_ebay: Optional[str] = "Sensoren"

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
        params = {}

        if self.category_id is not None:
            params["category"] = self.category_id

        if self.product_id is not None:
            params["include"] = self.product_id

        if self.name:
            params["search"] = self.name

        if self.sku:
            params["sku"] = self.sku

        if self.status:
            params["status"] = self.status

        if self.stock_status:
            params["stock_status"] = self.stock_status

        self.filter = urlencode(params)

    # --
    # ...
    # --

    def get_all_attributes(self):
        return asdict(self)
