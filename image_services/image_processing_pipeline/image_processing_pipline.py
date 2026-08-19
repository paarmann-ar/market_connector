import CONSTS
from image_services.background_operation.background_operation import BackgroundOperation
from image_services.cloud_operation.cloud_operation import CloudOperation
from image_services.cloud_operation.config.cloud_operation_config import CloudOperationConfig
from image_services.core.base import Base
from image_services.models.image_data_model import ImageDataModel
from toolboxs.random_expertion import RandomExpertion
from toolboxs.file_and_folder_operation import FileAndFolderOperation
from image_services.models.image_directory_model import ImageDirectoryModel

# --
# ...
# --


class ImageProcessingPipline(Base):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.images_address = f"{CONSTS.ROOT_DIR}{self.config_dictionary.get('images_address')}"
        FileAndFolderOperation.remove_nestet_folder(self.images_address)

        self.cloud_operation = CloudOperation()
        self.background_operation = BackgroundOperation()

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
