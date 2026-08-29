import json
from dataclasses import asdict, dataclass
from typing import Any, Optional


# --
# ...
# --


@dataclass
class ZalandoLoungeMediaModel:
    character_code: Optional[str] = None
    media_type: Optional[str] = None
    alt_text: Optional[str] = None
    path: Optional[str] = None
    sortKey: Optional[int] = None

    # --
    # ...
    # --

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    # --
    # ...
    # --
    def to_json(self) -> str:
        return json.dumps(
            self.to_dict(),
            ensure_ascii=False,
        )

    # --
    # ...
    # --

    @classmethod
    def from_api(
        cls,
        data: dict[str, Any],
    ) -> "ZalandoLoungeMediaModel":

        return cls(
            character_code=data.get("character_code"),
            media_type=data.get("media_type"),
            alt_text=data.get("alt_text"),
            path=data.get("path"),
            sortKey=data.get("sortKey"),
        )
