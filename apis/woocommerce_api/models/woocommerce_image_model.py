import json
from dataclasses import asdict, dataclass
from typing import Optional
from pydantic import BaseModel, ConfigDict

# --
# ...
# --


class WoocommerceImageModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: Optional[int] = None
    src: Optional[str] = None
    name: Optional[str] = None
    alt: Optional[str] = None
    srcset: Optional[str] = None

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

    # @classmethod
    # def from_api(cls, data):
    #     return cls(
    #         id=data.get("id"),
    #         name=data.get("name"),
    #         src=data.get("src"),
    #         alt=data.get("alt"),
    #         srcset=data.get("srcset")
    #     )

    @classmethod
    def from_api(cls, data: dict):
        return cls(
            id=data.get("id"),
            src=data.get("src"),
            name=data.get("name"),
            alt=data.get("alt"),
            srcset=data.get("srcset"),
        )
