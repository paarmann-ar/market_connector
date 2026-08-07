import json
from dataclasses import asdict, dataclass
from typing import Optional

# --
# ...
# --


@dataclass
class WoocommerceReviewModel:
    product_id: Optional[int] = None
    review: Optional[str] = None
    reviewer: Optional[str] = None
    reviewer_email: Optional[str] = None
    rating: Optional[int] = None

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
            product_id=data["product_id"],
            review=data["review"],
            reviewer=data["reviewer"],
            reviewer_email=data["reviewer_email"],
            rating=data["rating"],
        )
