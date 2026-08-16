import os

from apis.apis_provider import ApisProvider
from apis.ebay_api.models.search_in_ebay_model import SearchInEbayModel
from apis.woocommerce_api.models.woocommerce_product_model import WoocommerceProductModel
from apis.wordpress_api.models.wordpress_media_model import WordpressMediaModel
from app.core.base import Base
from image_services.models.image_data_model import ImageDataModel
from toolboxs.file_and_folder_operation import FileAndFolderOperation
from apis.ebay_api.models.product_ebay_model import ProductEbayModel

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

    def fetch_from_ebay(self, search_in_ebay_model: SearchInEbayModel)->list[ProductEbayModel]:
        product_ebay_models = self.apis_provider.ebay_api.fetch_product_from_ebay_by_search_in_ebay_model(search_in_ebay_model=search_in_ebay_model)

        return product_ebay_models
    
    # --
    # ...
    # --

    def convert_ebay_to_woocommerce_product_model(self, product_ebay_models:list[ProductEbayModel]) -> list[WoocommerceProductModel]:
        # ebay_product_detail_model_list = self.apis_provider.ebay_api.product_detail_list
        return self.apis_provider.woocommerce_api.convert_ebay_product_model_to_woocommerce_product_model(
            product_ebay_models=product_ebay_models
        )

    # --
    # ...
    # --

    def image_convertor_pipline(self, woocommerce_product_models:list[WoocommerceProductModel])->None:

        for woocommerce_product_model in woocommerce_product_models:
            image_data_models: list[ImageDataModel] = []
            wordpress_media_models: list[WordpressMediaModel] = []

            for woocommerce_product_model_image in woocommerce_product_model.images:
                image_data_model = ImageDataModel(
                    image_url=woocommerce_product_model_image.src, is_main_image=woocommerce_product_model_image.is_main_image
                )
                image_data_models.append(image_data_model)

            self.image_provider.image_processing_pipline.download_url_remove_white_bg_image(image_data_models=image_data_models)

            for image_data_model in image_data_models:
                wordpress_media_model = WordpressMediaModel(
                    media_address=image_data_model.images_address, media_name=image_data_model.image_name
                )
                wordpress_media_models.append(wordpress_media_model)

            source_urls = self.apis_provider.wordpress_api.upload_media_models_from_disk(media_models=wordpress_media_models)
            # main image ro ba if bezaram
            for image, url in zip(woocommerce_product_model.images, source_urls):
                image.src = url

            FileAndFolderOperation.remove_nestet_folder(self.image_provider.image_processing_pipline.images_address)
        

    # --
    # ...
    # --

    def upload_model_to_woocommerce(self, woocommerce_product_models :list[WoocommerceProductModel], search_in_ebay_model: SearchInEbayModel) -> bool:
        self.apis_provider.woocommerce_api.upload_product_model_to_woocommerce(woocommerce_product_models = woocommerce_product_models, target_woocommerce_category_name = search_in_ebay_model.target_category_name_in_woocommerce)
