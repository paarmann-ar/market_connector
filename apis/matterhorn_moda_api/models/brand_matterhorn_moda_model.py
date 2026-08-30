from typing import Optional
from pydantic import BaseModel

# --
# ...
# --


class BrandMatterhornModaModel(BaseModel):
    brand_id: Optional[str] = None
    brand_name: Optional[str] = None
    product_count: Optional[str] = None
