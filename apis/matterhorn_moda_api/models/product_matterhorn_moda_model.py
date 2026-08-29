from typing import Optional
from pydantic import BaseModel

# --
# ...
# --

class Price(BaseModel):
    EUR: Optional[float] = None
    CHF: Optional[float] = None
    CZK: Optional[float] = None
    USD: Optional[float] = None
    RUB: Optional[float] = None
    CAD: Optional[float] = None
    AUD: Optional[float] = None
    GBP: Optional[float] = None
    BGN: Optional[float] = None
    DKK: Optional[float] = None
    NOK: Optional[float] = None
    RON: Optional[float] = None
    SEK: Optional[float] = None
    HUF: Optional[float] = None


class ProductMatterhornModaModel(BaseModel):
    id: Optional[str] = None
    active: Optional[bool] = None
    name: Optional[str] = None
    name_without_number: Optional[str] = None
    description: Optional[str] = None
    creation_date: Optional[str] = None
    color: Optional[str] = None
    category_name: Optional[str] = None
    category_id: Optional[str] = None
    category_path: Optional[str] = None
    brand_id: Optional[str] = None
    brand: Optional[str] = None
    stock_total: Optional[int] = None
    url: Optional[str] = None

    images: Optional[list[str]] = None
    new_collection: Optional[str] = None

    variants: Optional[list] = None
    size_table: Optional[str] = None
    weight: Optional[int] = None
    products_in_set: Optional[list[str]] = None
    other_colors: Optional[list] = None

    prices: Optional[Price] = None

    size_table_txt: Optional[str] = None
    size_table_html: Optional[str] = None