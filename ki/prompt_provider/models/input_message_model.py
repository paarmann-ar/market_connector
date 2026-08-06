import json
from dataclasses import asdict, dataclass
from typing import Optional

# --
# ...
# --


@dataclass
class InputMessageModel:
    md_file_name: Optional[str] = None
    inputs: Optional[dict] = None

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
