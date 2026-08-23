import json
from dataclasses import asdict, dataclass, fields
from typing import Any, Optional

# --
# ...
# --


@dataclass
class ProductOutputMetadataModel:
    title: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    meta_description: Optional[str] = None
    focus_keywords: Optional[str] = None
    primary_focus_keyword: Optional[str] = None
    seo_model: Optional[Any] = None
    image_seo_model: Optional[Any] = None
    slug: Optional[Any] = None

    # --
    # ...
    # --

    def __init__(self, **kwargs):

        valid_fields = {field.name for field in fields(self)}

        for key, value in kwargs.items():
            # Ignore unknown fields
            if key not in valid_fields:
                continue

            setattr(self, key, value)

    # --
    # ...
    # --

    def to_dict(self) -> dict[str, Any]:

        data = asdict(self)
        return {key: value for key, value in data.items() if value is not None}

    # --
    # ...
    # --

    def to_json(self) -> str:

        return json.dumps(
            self.to_dict(),
            ensure_ascii=False,
        )
