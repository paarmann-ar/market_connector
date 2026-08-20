import json
from dataclasses import asdict, dataclass, fields
from typing import Optional

from apis.ebay_api.models.browse.product_summery_ebay_model import ProductSummeryEbayModel

# --
# ...
# --


@dataclass
class ProductsSummeryEbayModel:
    product_summery_ebay_model: Optional[ProductSummeryEbayModel] = None
    total: Optional[int] = None
    limit: Optional[int] = None
    offset: Optional[int] = None
    href: Optional[str] = None

    def __init__(self, **kwargs):
        valid_fields = {f.name for f in fields(self)}

        for key, value in kwargs.items():
            if key in valid_fields:
                setattr(self, key, value)

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
