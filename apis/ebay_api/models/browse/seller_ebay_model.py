import json
from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class SellerEbayModel:
    username: Optional[str] = None
    feedbackScore: Optional[int] = None
    feedbackPercentage: Optional[str] = None
    imageUrl: Optional[str] = None
    width: Optional[str] = None
    height: Optional[str] = None

    def to_json(self) -> str:
        return json.dumps(
            asdict(self),
            ensure_ascii=False,
        )

    def to_dict(self) -> dict:
        return asdict(self)
