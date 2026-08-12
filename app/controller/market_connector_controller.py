import os

from apis.apis_provider import ApisProvider
from apis.ebay_api.models.search_in_ebay_model import SearchInEbayModel
from apis.woocommerce_api.models.woocommerce_product_model import WoocommerceProductModel
from apis.wordpress_api.models.wordpress_media_model import WordpressMediaModel
from app.core.base import Base
from image_services.image_processing_pipeline.image_processing_pipline import ImageProcessingPipline
from image_services.models.image_data_model import ImageDataModel
from toolboxs.file_and_folder_operation import FileAndFolderOperation
# --
# ...
# --


class MarketConnectorController(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.apis_provider = ApisProvider()
        self.woocommerce_product_models: list[WoocommerceProductModel] = []

    # --
    # ...
    # --

    def fetch_from_ebay(self, search_in_ebay_model: SearchInEbayModel):
        self.apis_provider.ebay_api.fetch_product_from_ebay_by_search_in_ebay_model(search_in_ebay_model=search_in_ebay_model)

    # --
    # ...
    # --

    def convert_ebay_to_woocommerce_product_model(self, price_anpassen) -> None:
        ebay_product_detail_model_list = self.apis_provider.ebay_api.product_detail_list
        self.woocommerce_product_models = self.apis_provider.woocommerce_api.convert_ebay_product_model_to_woocommerce_product_model(
            ebay_product_detail_model_list=ebay_product_detail_model_list,
            price_anpassen=price_anpassen,
        )

    # --
    # ...
    # --

    def image_convertor_pipline(self):
        image_processing_pipline = ImageProcessingPipline()

        for woocommerce_product_model in self.woocommerce_product_models:
            image_data_models: list[ImageDataModel] = []
            wordpress_media_models: list[WordpressMediaModel] = []

            for woocommerce_product_model_image in woocommerce_product_model.images:
                image_data_model = ImageDataModel(
                    image_url=woocommerce_product_model_image.src, is_main_image=woocommerce_product_model_image.is_main_image
                )
                image_data_models.append(image_data_model)

            image_processing_pipline.download_url_remove_white_bg_image(image_data_models=image_data_models)

            for image_data_model in image_data_models:
                wordpress_media_model = WordpressMediaModel(
                    media_address=image_data_model.images_address, media_name=image_data_model.image_name
                )
                wordpress_media_models.append(wordpress_media_model)

            source_urls = self.apis_provider.wordpress_api.upload_media_models_from_disk(media_models=wordpress_media_models)
            # main image ro ba if bezaram
            for image, url in zip(woocommerce_product_model.images, source_urls):
                image.src = url

    # --
    # ...
    # --

    def upload_model_to_woocommerce(self, target_woocommerce_category_name: str) -> bool:
        self.apis_provider.woocommerce_api.upload_product_model_to_woocommerce(target_woocommerce_category_name)
