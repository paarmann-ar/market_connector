from image_services.core.base import Base
from image_services.cloud_operation.config.cloud_operation_config import CloudOperationConfig
from image_services.models.image_data_model import ImageDataModel
from image_services.background_operation.background_operation import BackgroundOperation
from image_services.cloud_operation.cloud_operation import CloudOperation
import CONSTS

# --
# ...
# --


class ImageProcessingPipline(Base):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.image_download_folder = f"{CONSTS.ROOT_DIR}{self.config_dictionary.get('output_folder')}"

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

    def download_url_remove_white_bg_image(self, image_data_models:list[ImageDataModel]) -> bool:

        try:
            for image_data_model in image_data_models:
                if not image_data_model.image_name:
                    image_data_model.image_name = image_data_model.input_image_url.split("/")[-1]

                if not image_data_model.output_image_adress:
                    image_data_model.output_image_adress= f"{self.image_download_folder}/{image_data_model.image_name}"

                image_data_model = self.cloud_operation.download_image_from_url(image_data_model)
                image_data_model.input_image_adress = image_data_model.output_image_adress
                image_data_model.output_image_adress = ""

            self.background_operation.remove_set_white_backgroung_on_photo()

            return True

        except Exception as exp:
            self.error(f"download_image: {exp}")

    # --
    # ...
    # --

ldm = ImageDataModel(input_image_url="https://i.ebayimg.com/images/g/S3YAAOSwZR5gWHWN/s-l1600.webp")
ImageProcessingPipline().download_url_remove_white_bg_image([ldm])