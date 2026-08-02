import json
from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class WordpressMediaModel:
    media_address: Optional[str] = None
    media_name: Optional[str] = None
    wp_id: Optional[int] = None
    wp_date: Optional[str] = None
    wp_title: Optional[str] = None
    wp_caption: Optional[str] = None
    wp_description: Optional[str] = None
    wp_alt_text: Optional[str] = None
    wp_slug: Optional[str] = None
    wp_post: Optional[str] = None
    wp_meta: Optional[str] = None
    wp_url: Optional[str] = None
    wp_link: Optional[str] = None
    wp_status: str = "inherit"

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

    # --
    # ...
    # --

    @classmethod
    def from_api(cls, data):
        return cls(
            media_address=data["media_address"],
            media_name=data["media_name"],
            wp_id=data["wp_id"],
            wp_date=data["wp_date"],
            wp_title=data["wp_title"],
            wp_caption=data["wp_caption"],
            wp_description=data["wp_description"],
            wp_alt_text=data["wp_alt_text"],
            wp_slug=data["wp_slug"],
            wp_post=data["wp_post"],
            wp_meta=data["wp_meta"],
            wp_url=data["wp_url"],
            wp_link=data["wp_link"],
            wp_status=data["wp_status"],
        )
