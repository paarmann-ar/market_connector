from apis.apis_provider import ApisProvider
from apis.ebay_api.models.browse.product_ebay_model import ProductEbayModel
from apis.ebay_api.models.search_in_ebay_model import SearchInEbayModel
from apis.woocommerce_api.models.woocommerce_product_model import WoocommerceProductModel

from market_services.adapters.ebay_product_model_to_woocommerce_product_model_adaptor import (
    EbayProductModelToWoocommerceProductModelAdaptor,
)
from market_services.image_services.image_processing_pipeline.image_processing_pipeline import (
    ImageProcessingPipeline,
)


class MarketConnectorController:
    """
    Controller responsible for connecting eBay and WooCommerce.
    """

    # -------------------------------------------------------------------------
    # eBay
    # -------------------------------------------------------------------------

    @staticmethod
    def fetch_from_ebay(
        search_in_ebay_model: SearchInEbayModel,
    ) -> list[ProductEbayModel]:
        """
        Fetch products from eBay based on the given search model.
        """

        return ApisProvider().ebay_api.pipeline_fetch_product_from_ebay_by_search_in_ebay_model(search_in_ebay_model=search_in_ebay_model)

    # -------------------------------------------------------------------------
    # WooCommerce
    # -------------------------------------------------------------------------

    @staticmethod
    def upload_to_woocommerce(
        woocommerce_product_models: list[WoocommerceProductModel],
        search_in_ebay_model: SearchInEbayModel,
    ) -> bool:
        """
        Upload WooCommerce products to the target WooCommerce category.
        """

        return ApisProvider().woocommerce_api.upload_product_model_to_woocommerce(
            woocommerce_product_models=woocommerce_product_models,
            target_woocommerce_category_name=(search_in_ebay_model.target_category_name_in_woocommerce),
        )

    # -------------------------------------------------------------------------
    # eBay -> WooCommerce
    # -------------------------------------------------------------------------

    @staticmethod
    def sync_ebay_to_woocommerce(
        search_in_ebay_model: SearchInEbayModel,
    ) -> bool:
        """
        Fetch products from eBay, convert them to WooCommerce models,
        process images and upload them to WooCommerce.
        """

        product_ebay_models = MarketConnectorController.fetch_from_ebay(search_in_ebay_model=search_in_ebay_model)

        if not product_ebay_models:
            return False

        woocommerce_product_models: list[WoocommerceProductModel] = []

        adaptor = EbayProductModelToWoocommerceProductModelAdaptor()

        for product_ebay_model in product_ebay_models:
            product_ebay_model.price_anpassen = search_in_ebay_model.price_anpassen

            woocommerce_product_model = adaptor.adapter(product_ebay_model=product_ebay_model)

            woocommerce_product_models.append(woocommerce_product_model)

        if not woocommerce_product_models:
            return False

        ImageProcessingPipeline().image_convertor_pipeline(woocommerce_product_models=woocommerce_product_models)

        return MarketConnectorController.upload_to_woocommerce(
            woocommerce_product_models=woocommerce_product_models,
            search_in_ebay_model=search_in_ebay_model,
        )

    # -------------------------------------------------------------------------
    # eBay -> eBay
    # -------------------------------------------------------------------------

    @staticmethod
    def create_ebay_offers(
        search_in_ebay_model: SearchInEbayModel,
    ) -> bool:
        """
        Fetch products from eBay and create offers on eBay.
        """

        product_ebay_models = MarketConnectorController.fetch_from_ebay(search_in_ebay_model=search_in_ebay_model)

        if not product_ebay_models:
            return False

        ebay_api = ApisProvider().ebay_api

        for product_ebay_model in product_ebay_models:
            product_ebay_model.price_anpassen = search_in_ebay_model.price_anpassen

            # TODO:
            # Generate a unique SKU instead of using a hard-coded value.
            product_ebay_model.sku = "im_US_ebay_0000001"

            ebay_api.pipeline_create_ebay_offer(
                product_ebay_model=product_ebay_model,
                marketplace_id="EBAY_DE",
            )

        return True


# from apis.apis_provider import ApisProvider
# from apis.ebay_api.models.browse.product_ebay_model import ProductEbayModel
# from apis.ebay_api.models.search_in_ebay_model import SearchInEbayModel
# from apis.woocommerce_api.models.woocommerce_product_model import WoocommerceProductModel
# from app.core.base import Base
# from app.controller.market_connector_controller import MarketConnectorController
# from market_services.adapters.ebay_product_model_to_woocommerce_product_model_adaptor import (
#     EbayProductModelToWoocommerceProductModelAdaptor,
# )
# from market_services.image_services.image_processing_pipeline.image_processing_pipeline import ImageProcessingPipeline

# # --
# # ...
# # --


# class MarketConnectorController:
#     # --
#     # ...
#     # --
#     @staticmethod
#     def fetch_from_ebay(search_in_ebay_model: SearchInEbayModel) -> list[ProductEbayModel]:
#         product_ebay_models = ApisProvider().ebay_api.pipeline_fetch_product_from_ebay_by_search_in_ebay_model(
#             search_in_ebay_model=search_in_ebay_model
#         )

#         return product_ebay_models

#     # --
#     # ...
#     # --

#     @staticmethod
#     def upload_model_to_woocommerce(
#         woocommerce_product_models: list[WoocommerceProductModel], search_in_ebay_model: SearchInEbayModel
#     ) -> bool:
#         ApisProvider().woocommerce_api.upload_product_model_to_woocommerce(
#             woocommerce_product_models=woocommerce_product_models,
#             target_woocommerce_category_name=search_in_ebay_model.target_category_name_in_woocommerce,
#         )

#     # --
#     # ...
#     # --

#     @staticmethod
#     def download_from_ebay_and_create_offer_on_woocommerce_pipeline(search_in_ebay_model: SearchInEbayModel):
#         market_connector_controller = MarketConnectorController()

#         product_ebay_models = market_connector_controller.fetch_from_ebay(search_in_ebay_model=search_in_ebay_model)

#         woocommerce_product_models: list[WoocommerceProductModel] = []
#         for product_ebay_model in product_ebay_models:
#             product_ebay_model.price_anpassen = search_in_ebay_model.price_anpassen

#             woocommerce_product_models.append(EbayProductModelToWoocommerceProductModelAdaptor().adapter(product_ebay_model=product_ebay_model))

#         ImageProcessingPipeline().image_convertor_pipeline(woocommerce_product_models=woocommerce_product_models)

#         market_connector_controller.upload_model_to_woocommerce(
#             woocommerce_product_models=woocommerce_product_models, search_in_ebay_model=search_in_ebay_model
#         )

#     # --
#     # ...
#     # --

#     @staticmethod
#     def download_from_ebay_and_create_offer_on_ebay_pipeline(search_in_ebay_model: SearchInEbayModel):
#         market_connector_controller = MarketConnectorController()

#         product_ebay_models = market_connector_controller.fetch_from_ebay(search_in_ebay_model=search_in_ebay_model)

#         for product_ebay_model in product_ebay_models:
#             product_ebay_model.price_anpassen = search_in_ebay_model.price_anpassen

#             product_ebay_model.sku = "im_US_ebay_0000001"
#             market_connector_controller.apis_provider.ebay_api.pipeline_create_ebay_offer(
#                 product_ebay_model=product_ebay_model, marketplace_id="EBAY_DE"
#             )

#         return
