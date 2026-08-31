import json
from dataclasses import asdict
from typing import Any, Optional

from pydantic import BaseModel

# --
# ...
# --


class ProductOutputMetadataModel(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    meta_description: Optional[str] = None
    focus_keywords: Optional[list[str]] = None
    primary_focus_keyword: Optional[str] = None
    seo_model: Optional[Any] = None
    image_seo_model: Optional[Any] = None
    slug: Optional[str] = None
    image_description: Optional[str] = None
    product_tags: Optional[list[str]] = None

    #  --
    #  ...
    #  --

    def to_dict(self) -> dict[str, Any]:

        data = asdict(self)
        return {key: value for key, value in data.items() if value is not None}

    #  --
    #  ...
    #  --

    def to_json(self) -> str:

        return json.dumps(
            self.to_dict(),
            ensure_ascii=False,
        )
