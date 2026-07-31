from dataclasses import dataclass, field, asdict
from apis.models.woocommerce_category_model import WoocommerceCategoryModel
from apis.models.woocommerce_image_model import WoocommerceImageModel
import json

# --
# ...
# --

@dataclass
class WoocommerceProductModel:
    id:int = 0
    name:str = ""
    slug:str = ""
    permalink:str = ""
    catalog_visibility:str = "visible"
    description:str =""
    short_description:str=""
    sku:str =""
    price:str = ""
    regular_price:str = ""
    sale_price:str=""
    on_sale:bool = False
    tax_status:str = "taxable"
    tax_class:str =""
    manage_stock:bool = False
    shipping_required:bool = True
    shipping_taxable:bool = True
    shipping_class:str =""
    shipping_class_id:int = 0
    categories: list[WoocommerceCategoryModel] = field(default_factory=list)
    brands: list[str] = field(default_factory=list)
    tags:list[str]=field(default_factory=list)
    images:list[WoocommerceImageModel]= field(default_factory=list)
    attributes:list= field(default_factory=list)
    default_attributes:list[str]=field(default_factory=list)
    stock_status:str = 'instock'

    # --
    # ...
    # --

    def to_json(self):
        return json.dumps(asdict(self), ensure_ascii=False)
    
    # --
    # ...
    # --

    def to_dict(self):
        return asdict(self)