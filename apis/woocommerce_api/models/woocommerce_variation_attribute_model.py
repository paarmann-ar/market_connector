from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


# --
# ...
# --


class WoocommerceVariationAttributeModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: Optional[int] = None
    name: Optional[str] = None
    option: Optional[str] = None


# --
# ...
# --


class WoocommerceVariationModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: Optional[int] = None

    sku: Optional[str] = None

    price: Optional[str] = None
    regular_price: Optional[str] = None
    sale_price: Optional[str] = None

    manage_stock: bool = False
    stock_quantity: Optional[int] = None
    stock_status: Optional[str] = "instock"

    attributes: list[WoocommerceVariationAttributeModel] = Field(default_factory=list)


