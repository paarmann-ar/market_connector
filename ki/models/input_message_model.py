import json
from dataclasses import asdict, dataclass, fields
from typing import Optional

from pydantic import BaseModel

# --
# ...
# --


@dataclass
class ProductInput(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    short_description: Optional[str] = None
    brand: Optional[str] = None
    condition: Optional[str] = None
    mpn: Optional[str] = None


# --
# ...
# --


@dataclass
class InputMessageModel:
    md_file_name: Optional[str] = None
    inputs: Optional[ProductInput] = None

    #  --
    #  ...
    #  --

    def __init__(self, **kwargs):

        valid_fields = {field.name for field in fields(self)}

        for key, value in kwargs.items():
            #  Ignore unknown fields
            if key not in valid_fields:
                continue

            setattr(self, key, value)

    #  --
    #  ...
    #  --

    def to_json(self):
        return json.dumps(asdict(self), ensure_ascii=False)

    #  --
    #  ...
    #  --

    def to_dict(self):
        data = asdict(self)
        return data
