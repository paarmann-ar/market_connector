from image_services.core.base import Base
from image_services.cloud_operation.config.cloud_operation_config import CloudOperationConfig
from image_services.models.image_data_model import ImageDataModel
from image_services.cloud_operation.services.download_image import DownloadImage
import CONSTS

# --
# ...
# --


class CloudOperation(Base):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

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

    def download_image_from_url(self, image_data_model:ImageDataModel) -> ImageDataModel:

        try:

            download_image = DownloadImage()
            download_image.download_image(image_data_model= image_data_model)
    
            return image_data_model

        except Exception as exp:
            self.error(f"download_image: {exp}")

    # --
    # ...
    # --
# CloudOperation().download_image_from_url(url="https://i.ebayimg.com/images/g/S3YAAOSwZR5gWHWN/s-l1600.webp")