import json
import re
from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class WoocommerceTagModel:
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
        return json.dumps(
            self.to_dict(),
            ensure_ascii=False,
        )

    # --
    # ...
    # --

    def to_dict(self) -> dict:
        data = asdict(self)
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

        # Replace spaces and special characters with "-"
        slug = re.sub(
            r"[^a-z0-9äöüß]+",
            "-",
            slug,
        )

        # Remove duplicate "-"
        slug = re.sub(
            r"-+",
            "-",
            slug,
        )

        return slug.strip("-").lower()
