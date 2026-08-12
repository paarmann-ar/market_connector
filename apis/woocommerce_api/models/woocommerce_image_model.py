import json
from dataclasses import asdict, dataclass
from typing import Optional

# --
# ...
# --


@dataclass
class WoocommerceImageModel:
    id: Optional[int] = None
    src: Optional[str] = None
    name: Optional[str] = None
    alt: Optional[str] = None
    srcset: Optional[str] = None
    is_main_image: bool = False

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
            is_main_image=data.get("is_main_image"),
        )
