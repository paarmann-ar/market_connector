from apis.apis_provider import ApisProvider
from apis.ebay_api.models.browse.product_ebay_model import ProductEbayModel
from apis.ebay_api.models.search_in_ebay_model import SearchInEbayModel
from apis.woocommerce_api.models.woocommerce_product_model import WoocommerceProductModel

from market_services.adapters.ebay.ebay_product_model_to_woocommerce_product_model_adaptor import (
    EbayProductModelToWoocommerceProductModelAdaptor,
)
from market_services.image_services.image_processing_pipeline.image_processing_pipeline import (
    ImageProcessingPipeline,
)
from apis.woocommerce_api.models.search_in_woocommerce_model import SearchInWoocommerceModel
from market_services.adapters.woocommerce.woocommerce_to_ebay_inventory_adapter import WoocommerceToEbayInventoryAdapter

from apis.zalando_lounge_api.models.search_in_zalando_lounge_model import SearchInZalandoLoungeModel

from apis.matterhorn_moda_api.models.search_in_matterhorn_moda_model import SearchInMatterhornModaModel
from apis.matterhorn_moda_api.models.product_matterhorn_moda_model import ProductMatterhornModaModel
from market_services.adapters.matterhorn.matterhorn_moda_product_model_to_woocommerce_product_model_adaptor import MatterhornModaProductModelToWoocommerceProductModelAdaptor

class MarketConnectorController:
    """
    Controller responsible for connecting eBay and WooCommerce.
    """

    # --
    # ...
    # --

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

    # --
    # ...
    # --

    @staticmethod
    def sync_ebay_to_woocommerce(
        search_in_ebay_model: SearchInEbayModel,
    ) -> None:
        """
        Fetch products from eBay, convert them to WooCommerce models,
        process images and upload them to WooCommerce.
        """

        product_ebay_models = ApisProvider().ebay_api.pipeline_fetch_product_from_ebay_by_search_in_ebay_model(
            search_in_ebay_model=search_in_ebay_model
        )

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

        MarketConnectorController.upload_to_woocommerce(
            woocommerce_product_models=woocommerce_product_models,
            search_in_ebay_model=search_in_ebay_model,
        )

    # --
    # ...
    # --

    @staticmethod
    def create_ebay_offers(
        search_in_ebay_model: SearchInEbayModel,
    ) -> bool:
        """
        Fetch products from eBay and create offers on eBay.
        """

        product_ebay_models = ApisProvider().ebay_api.pipeline_fetch_product_from_ebay_by_search_in_ebay_model(
            search_in_ebay_model=search_in_ebay_model
        )

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

    # --
    # ...
    # --

    @staticmethod
    def sync_woocommerce_to_ebay(
        search_in_woocommerce_model: SearchInWoocommerceModel,
    ) -> bool:
        """
        Fetch products from woocommerce and create offers on eBay.
        """

        woocommerce_api = ApisProvider().woocommerce_api

        product_woocommerce_models = woocommerce_api.fetch_from_woocommerce(search_in_woocommerce_model=search_in_woocommerce_model)

        for product_woocommerce_model in product_woocommerce_models:
            woocommerce_to_ebay_inventory_adapter = WoocommerceToEbayInventoryAdapter(woocommerce_product=product_woocommerce_model).adapt()
            # az inja bayad sku ezafeh konam badan minvisam

            print(woocommerce_to_ebay_inventory_adapter)

    # --
    # ...
    # --

    @staticmethod
    def sync_zalando_lounge_to_woocommerce(
        search_in_zalando_lounge_model: SearchInZalandoLoungeModel,
    ) -> bool:
        """
        Fetch products from zalando lounge and sync to woocommerce.
        """

        zalando_lounge_api = ApisProvider().zalando_lounge_api

        product_woocommerce_models = zalando_lounge_api.fetch_from_zalando_lounge(search_in_zalando_lounge_model)

        # for product_woocommerce_model in product_woocommerce_models:
        #     woocommerce_to_ebay_inventory_adapter = WoocommerceToEbayInventoryAdapter(woocommerce_product=product_woocommerce_model).adapt()
        #     # az inja bayad sku ezafeh konam badan minvisam

        #     print(woocommerce_to_ebay_inventory_adapter)

    @staticmethod
    def sync_matterhorn_moda_to_woocommerce(search_in_matterhorn_moda_model:SearchInMatterhornModaModel):
        matterhorn_moda_api = ApisProvider().matterhorn_moda_api
        product_matterhorn_moda_models = matterhorn_moda_api.pipeline_fetch_products_from_matterhorn_moda()

        woocommerce_product_models: list[WoocommerceProductModel] = []
        adaptor = MatterhornModaProductModelToWoocommerceProductModelAdaptor()

        for product_matterhorn_moda_model in product_matterhorn_moda_models[:3]:
            product_matterhorn_moda_model.prices.EUR= product_matterhorn_moda_model.prices.EUR * search_in_matterhorn_moda_model.price_anpassen
            woocommerce_product_model = adaptor.adapter(product_matterhorn_moda_model=product_matterhorn_moda_model)
            woocommerce_product_models.append(woocommerce_product_model)

        ImageProcessingPipeline().image_convertor_pipeline(woocommerce_product_models=woocommerce_product_models,is_remove_set_white_backgroung_on_photo=False, download_url_remove_white_bg_image=False)

        MarketConnectorController.upload_to_woocommerce(
            woocommerce_product_models=woocommerce_product_models,
            search_in_ebay_model=search_in_matterhorn_moda_model,
        )
