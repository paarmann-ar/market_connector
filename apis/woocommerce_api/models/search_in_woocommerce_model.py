from typing import Optional
from pydantic import BaseModel


# --
# ...
# --
class SearchInWoocommerceModel(BaseModel):
    category_name_candidate: Optional[str] = None
    category_id: Optional[int] = None
    product_id: Optional[int] = None
    name: Optional[str] = None
    sku: Optional[str] = None
    status: Optional[str] = None
    stock_status: Optional[str] = None
    filter: Optional[str] = None
    item_id: Optional[str] = None
    total: Optional[int] = None
    item_to_fetch: int = 5
    price_anpassen: float = 1.60
    target_category_name_in_ebay: str = "Sensoren"

    # --
    # ...
    # --

    def __post_init__(self):
        self.generate_filter()

    # --
    # ...
    # --

    def to_dict(self):
        return self.model_dump(exclude_none=True)

    # --
    # ...
    # --

    def to_json(self):
        return self.model_dump_json()

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

        self.filter = params
