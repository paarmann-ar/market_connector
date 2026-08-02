import json
from dataclasses import asdict, dataclass, field
from typing import Optional

from apis.woocommerce_api.models.woocommerce_image_model import WoocommerceImageModel

# --
# ...
# --


@dataclass
class WoocommerceCategoryModel:
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    images: list[WoocommerceImageModel] = field(default_factory=list)

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
            id=data["id"],
            name=data["name"],
            slug=data["slug"],
            description=data["description"],
            images=data.get("images", None),
        )
