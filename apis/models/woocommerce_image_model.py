from dataclasses import dataclass,asdict
import json

# --
# ...
# --

@dataclass
class WoocommerceImageModel:
    id:int = 0
    src:str = "" 
    name:str = ""
    alt:str =""
    srcset:str =""


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