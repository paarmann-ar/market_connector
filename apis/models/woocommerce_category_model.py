from dataclasses import dataclass,asdict
import json

# --
# ...
# --

@dataclass
class WoocommerceCategoryModel:
    id:int = 0
    name:str = ""
    slug:str = ""


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