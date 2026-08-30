import json
from dataclasses import asdict, dataclass, field
from typing import Optional
from pydantic import BaseModel, ConfigDict
from apis.woocommerce_api.models.woocommerce_image_model import WoocommerceImageModel

# --
# ...
# --


class WoocommerceCategoryModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    parent_id: Optional[int] = None
    path: Optional[str] = None
    images: list[WoocommerceImageModel] = field(default_factory=list)

    # --
    # ...
    # --

    @classmethod
    def from_api(cls, data):
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            slug=data.get("slug"),
            description=data.get("description"),
            parent_id=data.get("parent", 0) or None,
            images=data.get("images") or [],
        )

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
