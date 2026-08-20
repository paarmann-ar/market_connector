import CONSTS
from apis.apis_provider import ApisProvider
from apis.woocommerce_api.models.woocommerce_product_model import WoocommerceProductModel
from apis.wordpress_api.models.wordpress_media_model import WordpressMediaModel
from market_services.image_services.background_operation.background_operation import BackgroundOperation
from market_services.image_services.cloud_operation.cloud_operation import CloudOperation
from market_services.image_services.cloud_operation.config.cloud_operation_config import CloudOperationConfig
from market_services.image_services.core.base import Base
from market_services.image_services.models.image_data_model import ImageDataModel
from market_services.image_services.models.image_directory_model import ImageDirectoryModel
from toolboxs.file_and_folder_operation import FileAndFolderOperation
from toolboxs.random_expertion import RandomExpertion

# --
# ...
# --


class ImageProcessingPipeline(Base):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.images_address = f"{CONSTS.ROOT_DIR}{self.config_dictionary.get('images_address')}"

        self.cloud_operation = CloudOperation()
        self.background_operation = BackgroundOperation()

        FileAndFolderOperation.remove_nestet_folder(self.images_address)
        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(self):
        return CloudOperationConfig().get_dictionary()

    # --
    # ...
    # --

    def download_url_remove_white_bg_image(self, image_data_models: list[ImageDataModel]) -> list[ImageDataModel]:

        try:
            for image_data_model in image_data_models:
                if not image_data_model.image_name:
                    image_name = RandomExpertion.get_uuid(postfix=".webp")
                    image_data_model.image_name = image_name

                if not image_data_model.images_address:
                    image_data_model.images_address = f"{self.images_address}/{image_data_model.image_name}"

                image_data_model = self.cloud_operation.download_image_from_url(image_data_model)

            image_data_models = self.background_operation.remove_set_white_backgroung_on_photo()

            return image_data_models

        except Exception as exp:
            self.error(f"download_image: {exp}")

    # --
    # ...
    # --

    def reduce_image_size(self, image_directory_model: ImageDirectoryModel):
        self.background_operation.reduce_image_size(image_directory_model)

    # --
    # ...
    # --

    def image_convertor_pipeline(self, woocommerce_product_models: list[WoocommerceProductModel]) -> None:

        for woocommerce_product_model in woocommerce_product_models:
            image_data_models: list[ImageDataModel] = []
            wordpress_media_models: list[WordpressMediaModel] = []

            for woocommerce_product_model_image in woocommerce_product_model.images:
                image_data_model = ImageDataModel(
                    image_url=woocommerce_product_model_image.src, is_main_image=woocommerce_product_model_image.is_main_image
                )
                image_data_models.append(image_data_model)

            self.download_url_remove_white_bg_image(image_data_models=image_data_models)

            for image_data_model in image_data_models:
                wordpress_media_model = WordpressMediaModel(
                    media_address=image_data_model.images_address, media_name=image_data_model.image_name
                )
                wordpress_media_models.append(wordpress_media_model)

            source_urls = ApisProvider().wordpress_api.upload_media_models_from_disk(media_models=wordpress_media_models)
            # main image ro ba if bezaram
            for image, url in zip(woocommerce_product_model.images, source_urls):
                image.src = url

            FileAndFolderOperation.remove_nestet_folder(self.images_address)
