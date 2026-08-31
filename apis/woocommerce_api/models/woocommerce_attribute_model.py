from typing import Optional
from pydantic import BaseModel, Field
# --
# ...
# --


class WoocommerceAttributeModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    type: Optional[str] = "select"
    order_by: Optional[str] = "menu_order"
    has_archives: Optional[bool] = False

    #  --
    #  ...
    #  --

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)

    #  --
    #  ...
    #  --

    def to_json(self) -> str:
        return self.model_dump_json()

    # --
    # ...
    # --

    @classmethod
    def from_api(cls, data: dict):

        return cls(
            id=data.get("id"),
            name=data.get("name"),
            slug=data.get("slug"),
            type=data.get("type"),
            order_by=data.get("order_by"),
            has_archives=data.get("has_archives"),
        )


# --
# ...
# --


class WoocommerceAttributeTermModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None

    #  --
    #  ...
    #  --

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)

    #  --
    #  ...
    #  --

    def to_json(self) -> str:
        return self.model_dump_json()

    # --
    # ...
    # --

    @classmethod
    def from_api(cls, data: dict):

        return cls(
            id=data.get("id"),
            name=data.get("name"),
            slug=data.get("slug"),
            description=data.get("description"),
            count=data.get("count", 0),
        )

    #  --
    #  ...
    #  --


class WoocommerceProductAttributeModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    options: list[str] = Field(default_factory=list)
    visible: bool = True
    variation: bool = False

    #  --
    #  ...
    #  --

    def to_dict(self) -> dict:
        return self.model_dump(exclude_none=True)

    #  --
    #  ...
    #  --

    def to_json(self) -> str:
        return self.model_dump_json()
