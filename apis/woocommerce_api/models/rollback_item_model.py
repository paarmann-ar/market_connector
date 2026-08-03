from dataclasses import dataclass
from typing import Optional

# --
# ...
# --


# type mishe category, product, tag, brand, media
@dataclass
class RollbackItem:
    type: Optional[str] = None
    id: Optional[int] = None
