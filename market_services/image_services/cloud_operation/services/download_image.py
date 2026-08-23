from market_services.image_services.cloud_operation.config.cloud_operation_config import CloudOperationConfig
from market_services.image_services.core.base import Base
from market_services.image_services.models.image_data_model import ImageDataModel
import re

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
            image_data_model.image_url = self.get_ebay_original_image_url(image_data_model.image_url)

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

    # --
    # ...
    # --

    def get_ebay_original_image_url(self, image_url: str) -> str:
        if not image_url:
            return image_url

        if "i.ebayimg.com" not in image_url:
            return image_url

        return re.sub(
            r"/s-l\d+\.jpg$",
            "/s-l1600.jpg",
            image_url,
            flags=re.IGNORECASE,
        )
