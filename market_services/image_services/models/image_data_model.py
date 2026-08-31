import json
from dataclasses import asdict, dataclass
from typing import Any, Optional

# --
# ...
# --


@dataclass
class ImageDataModel:
    image_name: Optional[str] = None
    images_address: Optional[str] = None
    image_url: Optional[str] = None
    alt: Optional[str] = None
    image_data: Optional[Any] = None
    image_size: Optional[tuple] = None
    product_box: Optional[tuple] = None
    mask: Optional[Any] = None
    image_description: Optional[str] = None

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

    #  --
    #  ...
    #  --

    def to_list(self):
        return [self]
