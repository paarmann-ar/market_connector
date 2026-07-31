from dataclasses import dataclass,asdict
import json

@dataclass
class WordpressMediaModel:
    media_address: str = ""
    media_name: str= ""
    wp_id: int= 0
    wp_date:str ='2026-07-15T10:37:21'
    wp_title: str= ""
    wp_caption: str= ""
    wp_description: str= ""
    wp_alt_text: str= ""
    wp_slug: str= ""
    wp_post: str= ""
    wp_meta: str= ""
    wp_url: str= ""
    wp_link: str= ""
    wp_status:str ="inherit"


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