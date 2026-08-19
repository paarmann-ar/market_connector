from dataclasses import dataclass
from typing import Any, Optional


# --
# ...
# --


@dataclass
class InventoryProductDetailsModel:
    title: Optional[str] = None
    description: Optional[str] = None

    imageUrls: Optional[list[str]] = None

    brand: Optional[str] = None
    mpn: Optional[str] = None
    gtin: Optional[str] = None
    epid: Optional[str] = None

    aspects: Optional[dict[str, list[str]]] = None

    videoIds: Optional[list[str]] = None

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {}

        if self.title is not None:
            data["title"] = self.title

        if self.description is not None:
            data["description"] = self.description

        if self.imageUrls is not None:
            data["imageUrls"] = self.imageUrls

        if self.brand is not None:
            data["brand"] = self.brand

        if self.mpn is not None:
            data["mpn"] = self.mpn

        if self.gtin is not None:
            data["gtin"] = self.gtin

        if self.epid is not None:
            data["epid"] = self.epid

        if self.aspects is not None:
            data["aspects"] = self.aspects

        if self.videoIds is not None:
            data["videoIds"] = self.videoIds

        return data
