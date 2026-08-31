from typing import Optional

from pydantic import BaseModel, ConfigDict

# --
# ...
# --


class WoocommerceBrandModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: Optional[int] = None
    name: Optional[str] = "No Brand"
    slug: Optional[str] = None
    description: Optional[str] = None

    #  --
    #  ...
    #  --

    def to_json(self):
        return self.model_dump_json()

    #  --
    #  ...
    #  --

    def to_dict(self):
        return self.model_dump(exclude_none=True)

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
