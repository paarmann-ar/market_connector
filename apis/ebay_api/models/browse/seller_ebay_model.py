import json
from dataclasses import asdict, dataclass, fields
from typing import Optional


@dataclass
class SellerEbayModel:
    username: Optional[str] = None
    feedbackScore: Optional[int] = None
    feedbackPercentage: Optional[str] = None
    imageUrl: Optional[str] = None
    width: Optional[str] = None
    height: Optional[str] = None

    #  --
    #  ...
    #  --

    def __init__(self, **kwargs):
        valid_fields = {f.name for f in fields(self)}

        for key, value in kwargs.items():
            if key in valid_fields:
                setattr(self, key, value)

    def to_json(self) -> str:
        return json.dumps(
            asdict(self),
            ensure_ascii=False,
        )

    def to_dict(self) -> dict:
        return asdict(self)
