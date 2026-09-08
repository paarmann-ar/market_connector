from pydantic import BaseModel
from typing import List


class VariantsMatterhornModeModel(BaseModel):
    variant_uid: int
    name: str
    stock: int
    max_processing_time: int
    ean: str
