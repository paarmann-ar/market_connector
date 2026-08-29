from typing import Optional

from pydantic import BaseModel

# --
# ...
# --


class CategoryMatterhornModaModel(BaseModel):
    category_id: Optional[int] = None
    category_name: Optional[str] = None
    category_path: Optional[str] = None