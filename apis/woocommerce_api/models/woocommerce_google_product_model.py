from typing import Optional, Literal

from pydantic import BaseModel, ConfigDict


class WoocommerceGoogleProductModel(BaseModel):
    model_config = ConfigDict(extra="ignore")

    manufacturer_part_number: Optional[str] = None

    condition: Optional[
        Literal["new", "refurbished", "used"]
    ] = None

    gender: Optional[
        Literal["male", "female", "unisex"]
    ] = None

    size: Optional[str] = None

    size_system: Optional[
        Literal[
            "US",
            "EU",
            "UK",
            "DE",
            "FR",
            "IT",
            "AU",
            "BR",
            "CN",
            "JP",
            "MX",
        ]
    ] = None

    size_type: Optional[
        Literal[
            "regular",
            "petite",
            "plus",
            "tall",
            "big",
            "maternity",
        ]
    ] = None

    color: Optional[str] = None

    material: Optional[str] = None

    pattern: Optional[str] = None

    age_group: Optional[
        Literal[
            "newborn",
            "infant",
            "toddler",
            "kids",
            "adult",
        ]
    ] = None

    multipack: Optional[int] = None

    is_bundle: Optional[bool] = None

    availability_date: Optional[str] = None

    adult_content: Optional[bool] = None

    # ------------------------------------------------------------------
    # WooCommerce Google for WooCommerce meta keys
    # ------------------------------------------------------------------

    META_KEYS = {
        "manufacturer_part_number": "_wc_gla_mpn",
        "condition": "_wc_gla_condition",
        "gender": "_wc_gla_gender",
        "size": "_wc_gla_size",
        "size_system": "_wc_gla_sizeSystem",
        "size_type": "_wc_gla_sizeType",
        "color": "_wc_gla_color",
        "material": "_wc_gla_material",
        "pattern": "_wc_gla_pattern",
        "age_group": "_wc_gla_ageGroup",
        "multipack": "_wc_gla_multipack",
        "is_bundle": "_wc_gla_isBundle",
        "availability_date": "_wc_gla_availabilityDate",
        "adult_content": "_wc_gla_adult",
    }

    def to_dict(self):
        return self.model_dump(exclude_none=True)

    def to_json(self):
        return self.model_dump_json()

    def to_meta_data(self) -> list[dict]:
        data = self.model_dump(exclude_none=True)

        return [
            {
                "key": self.META_KEYS[field_name],
                "value": value,
            }
            for field_name, value in data.items()
            if field_name in self.META_KEYS
        ]