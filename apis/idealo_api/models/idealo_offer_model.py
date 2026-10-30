from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field

# --
# ...
# --


class IdealoEnergyLabelModel(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    efficiency_class: Optional[str] = Field(
        default=None,
        alias="efficiencyClass",
    )
    spectrum: Optional[str] = None
    label_url: Optional[str] = Field(
        default=None,
        alias="labelUrl",
    )
    data_sheet_url: Optional[str] = Field(
        default=None,
        alias="dataSheetUrl",
    )
    fuel_efficiency_class: Optional[str] = Field(
        default=None,
        alias="fuelEfficiencyClass",
    )
    wet_grip_class: Optional[str] = Field(
        default=None,
        alias="wetGripClass",
    )
    external_rolling_noise: Optional[int] = Field(
        default=None,
        alias="externalRollingNoise",
    )
    external_rolling_noise_class: Optional[str] = Field(
        default=None,
        alias="externalRollingNoiseClass",
    )
    snow_grip: Optional[bool] = Field(
        default=None,
        alias="snowGrip",
    )
    ice_grip: Optional[bool] = Field(
        default=None,
        alias="iceGrip",
    )
    version: Optional[int] = None


# --
# ...
# --


class IdealoOfferModel(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    sku: Optional[str] = None
    title: Optional[str] = None
    price: Optional[str] = None
    former_price: Optional[str] = Field(
        default=None,
        alias="formerPrice",
    )
    url: Optional[str] = None

    payment_costs: Optional[Dict[str, str]] = Field(
        default=None,
        alias="paymentCosts",
    )
    delivery_costs: Optional[Dict[str, str]] = Field(
        default=None,
        alias="deliveryCosts",
    )

    base_price: Optional[str] = Field(
        default=None,
        alias="basePrice",
    )
    packaging_unit: Optional[int] = Field(
        default=None,
        alias="packagingUnit",
    )
    voucher_code: Optional[str] = Field(
        default=None,
        alias="voucherCode",
    )
    branch_id: Optional[str] = Field(
        default=None,
        alias="branchId",
    )

    brand: Optional[str] = None
    oens: Optional[List[str]] = None

    category_path: Optional[List[str]] = Field(
        default=None,
        alias="categoryPath",
    )

    description: Optional[str] = None

    image_urls: Optional[List[str]] = Field(
        default=None,
        alias="imageUrls",
    )

    eans: Optional[List[str]] = None
    hans: Optional[List[str]] = None
    pzns: Optional[List[str]] = None
    kbas: Optional[List[str]] = None

    merchant_name: Optional[str] = Field(
        default=None,
        alias="merchantName",
    )
    merchant_id: Optional[str] = Field(
        default=None,
        alias="merchantId",
    )

    delivery_comment: Optional[str] = Field(
        default=None,
        alias="deliveryComment",
    )
    delivery: Optional[str] = None

    max_order_processing_time: Optional[int] = Field(
        default=None,
        alias="maxOrderProcessingTime",
    )
    free_return_days: Optional[int] = Field(
        default=None,
        alias="freeReturnDays",
    )

    fulfillment_type: Optional[str] = Field(
        default=None,
        alias="fulfillmentType",
    )

    two_man_handling_fee: Optional[str] = Field(
        default=None,
        alias="twoManHandlingFee",
    )
    disposal_fee: Optional[str] = Field(
        default=None,
        alias="disposalFee",
    )

    eec: Optional[str] = None

    energy_labels: Optional[List[IdealoEnergyLabelModel]] = Field(
        default=None,
        alias="energyLabels",
    )

    deposit: Optional[str] = None
    size: Optional[str] = None
    colour: Optional[str] = None
    gender: Optional[str] = None
    material: Optional[str] = None

    replica: Optional[bool] = None
    used: Optional[bool] = None

    condition: Optional[str] = None
    condition_type: Optional[str] = Field(
        default=None,
        alias="conditionType",
    )

    download: Optional[bool] = None

    dynamic_product_attributes: Optional[Dict[str, List[str]]] = Field(
        default=None,
        alias="dynamicProductAttributes",
    )

    # --
    # ...
    # --

    def to_dict(self, exclude_none: bool = True) -> Dict[str, Any]:
        """
        Convert model to Idealo-compatible dictionary.
        """
        return self.model_dump(
            by_alias=True,
            exclude_none=exclude_none,
        )

    # --
    # ...
    # --

    def to_json(self, exclude_none: bool = True) -> str:
        """
        Convert model to JSON string.
        """
        return self.model_dump_json(
            by_alias=True,
            exclude_none=exclude_none,
        )
