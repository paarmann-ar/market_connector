import json
from dataclasses import asdict, dataclass
from typing import Optional

import CONSTS

# --
# ...
# --


@dataclass
class ImageDirectoryModel:
    images_folder_adress: Optional[str] = CONSTS.DOWNLOAD_DIR

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
