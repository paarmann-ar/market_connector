from typing import Optional

from pydantic import BaseModel

# --
# ...
# --


class WoocommerceReviewModel(BaseModel):
    product_id: Optional[int] = None
    review: Optional[str] = None
    reviewer: Optional[str] = None
    reviewer_email: Optional[str] = None
    rating: Optional[int] = None

    #  --
    #  ...
    #  --

    def to_dict(self):
        return self.model_dump(exclude_none=True)

    #  --
    #  ...
    #  --

    def to_json(self):
        return self.model_dump_json()

    #  --
    #  ...
    #  --

    @classmethod
    def from_api(cls, data):
        return cls(
            product_id=data["product_id"],
            review=data["review"],
            reviewer=data["reviewer"],
            reviewer_email=data["reviewer_email"],
            rating=data["rating"],
        )
