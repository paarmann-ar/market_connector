from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel

# --
# ...
# --

class RollbackItem(BaseModel):
    type: Optional[str] = None
    id: Optional[int] = None
