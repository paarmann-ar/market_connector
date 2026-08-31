import json
from dataclasses import asdict, dataclass
from typing import Annotated, Optional

from pydantic import BaseModel, Field

# --
# ...
# --


class ProductOutputModel(BaseModel):
    german_title: str
    english_title: str

    german_description: str
    english_description: str

    german_short_description: str
    english_short_description: str

    german_meta_description: str
    english_meta_description: str

    german_focus_keywords: Annotated[list[str], Field(min_length=1, max_length=4)]
    english_focus_keywords: Annotated[list[str], Field(min_length=1, max_length=4)]

    german_primary_focus_keyword: str
    english_primary_focus_keyword: str

    slug_components: Annotated[list[str], Field(min_length=5, max_length=5)]

    german_image_description: str
    english_image_description: str

    german_product_tags: list[str]
    english_product_tags: list[str]


# --
# ...
# --


@dataclass
class OllamaAnswerModel:
    answer: Optional[ProductOutputModel] = None

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
