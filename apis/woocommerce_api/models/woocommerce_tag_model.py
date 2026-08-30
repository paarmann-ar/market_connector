import json
import re
from typing import Optional
from pydantic import BaseModel

# --
# ...
# --


class WoocommerceTagModel(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None

    # --
    # ...
    # --

    @property
    def slug(self) -> str:
        return self.build_slug(self.name or "")

    # --
    # ...
    # --

    def to_json(self) -> str:
        return self.model_dump_json(exclude_none=True)

    # --
    # ...
    # --

    def to_dict(self) -> dict:
        data = self.model_dump(
            exclude_none=True,
        )

        data["slug"] = self.slug

        return data

    # --
    # ...
    # --

    @classmethod
    def from_api(cls, data: dict):
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
        )

    # --
    # ...
    # --

    @classmethod
    def build_slug(cls, name: str) -> str:

        if not name:
            return ""

        slug = name.lower()

        slug = re.sub(
            r"[^a-z0-9äöüß]+",
            "-",
            slug,
        )

        slug = re.sub(
            r"-+",
            "-",
            slug,
        )

        return slug.strip("-")
