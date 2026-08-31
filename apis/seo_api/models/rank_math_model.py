import json
from dataclasses import asdict, dataclass
from typing import Optional

# --
# ...
# --


# type mishe category, product, tag, brand, media
@dataclass
class RankMathModel:
    rank_math_title: Optional[str] = None
    rank_math_description: Optional[str] = None
    rank_math_focus_keyword: Optional[str] = None
    rank_math_canonical_url: Optional[str] = None
    rank_math_robots: Optional[str] = None

    #  --
    #  ...
    #  --

    def to_json(self):
        return json.dumps(asdict(self), ensure_ascii=False)

    #  --
    #  ...
    #  --

    def to_dict(self):
        return asdict(self)

    #  --
    #  ...
    #  --

    def clear(self):
        self.rank_math_title = None
        self.rank_math_description = None
        self.rank_math_focus_keyword = None
        self.rank_math_canonical_url = None
        self.rank_math_robots = None

    #  --
    #  ...
    #  --

    def for_use_in_woocommerce(self):

        try:
            data = asdict(self)

            data = [
                {
                    "key": "rank_math_title",
                    "value": data.get("rank_math_title", ""),
                },
                {
                    "key": "rank_math_description",
                    "value": data.get("rank_math_description", ""),
                },
                {
                    "key": "rank_math_focus_keyword",
                    "value": data.get("rank_math_focus_keyword", ""),
                },
                {
                    "key": "rank_math_canonical_url",
                    "value": data.get("rank_math_canonical_url", ""),
                },
            ]

            return data

        except Exception as exp:
            self.error(f"for_use_in_woocommerce: {exp}")

    #  --
    #  ...
    #  --

    @classmethod
    def from_api(cls, data):
        return cls(
            id=data["id"],
            name=data["name"],
            slug=data["slug"],
            description=data["description"],
        )
