from dataclasses import asdict, dataclass
from typing import Optional
from pydantic import BaseModel,ConfigDict
# --
# ...
# --


class ValidateFinalModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    validation_roles: Optional[list[str]] = []