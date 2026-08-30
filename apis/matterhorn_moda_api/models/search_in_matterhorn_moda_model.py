import json
from dataclasses import asdict, dataclass
from typing import Optional
from market_services.adapters.models.validate_final_model import ValidateFinalModel

# --
# ...
# --


@dataclass
class SearchInMatterhornModaModel:
    category_name_candidate: Optional[str] = None
    category_id = Optional[int]
    product_id = Optional[int]
    marketplace: Optional[str] = "EBAY_DE"
    marketplace_id: Optional[str] = "EBAY_DE"
    deliveryCountry: Optional[str] = "DE"
    conditions: Optional[str] = "{NEW|USED}"
    filter: Optional[str] = None
    q: Optional[str] = None
    legacy_item_id: Optional[str] = None
    total: Optional[int] = None
    item_to_fetch: Optional[int] = 5
    price_anpassen: Optional[int] = 1.60
    sale_price_anpassen: Optional[int] = 1.50
    target_category_name_in_woocommerce: Optional[str] = None
    is_remove_description_html: Optional[bool] = True

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
