import json
from dataclasses import asdict, dataclass, fields
from typing import Any, Optional

# --
# ...
# --


@dataclass
class ProductInputMetadataModel:
    prompt_filename: Optional[str] = "prompt"
    cache_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    brand: Optional[str] = None
    condition: Optional[str] = None
    mpn: Optional[str] = None

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
