import json
from dataclasses import asdict, dataclass
from typing import Optional, Any

# --
# ...
# --


@dataclass
class ImageDirectoryModel:
    images_folder_adress: Optional[str] = None

    # --
    # ...
    # --

    def to_json(self):
        return json.dumps(asdict(self), ensure_ascii=False)

    # --
    # ...
    # --

    def to_dict(self):
        data = asdict(self)
        return data

    # --
    # ...
    # --

    def to_list(self):
        return [self]
