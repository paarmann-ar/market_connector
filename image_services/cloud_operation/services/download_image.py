from image_services.cloud_operation.config.cloud_operation_config import CloudOperationConfig
from image_services.core.base import Base
from image_services.models.image_data_model import ImageDataModel

# --
# ...
# --


class DownloadImage(Base):
    def __init__(self, **kwargs):
        super(**kwargs).__init__(**kwargs)

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return CloudOperationConfig().get_dictionary()

    # --
    # ...
    # --

    def __call__(self) -> str:
        pass

    # ...
    # --

    def download_image(self, image_data_model: ImageDataModel) -> ImageDataModel:

        try:
            response = self.request(
                method="get",
                url=image_data_model.image_url,
                is_download_file=True,
                download_file_address=f"{image_data_model.images_address}",
            )

            image_data_model.image_data = response
            self.prompt_on_screen(f"download_image: {response}")

            return image_data_model

        except Exception as exp:
            self.prompt_on_screen(f"download_image: {exp}")
