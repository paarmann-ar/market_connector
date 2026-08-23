from pathlib import Path

from PIL import Image

from market_services.image_services.background_operation.config.background_operation_config import BackgroundOperationConfig
from market_services.image_services.core.base import Base
from market_services.image_services.models.image_data_model import ImageDataModel
from market_services.image_services.models.image_directory_model import ImageDirectoryModel

# --
# ...
# --


class PrepaerImageFile(Base):
    def __init__(self, **kwargs):
        super(**kwargs).__init__(**kwargs)

        self.cache_file_name = self.config_dictionary.get("cache_file_name")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return BackgroundOperationConfig().get_dictionary()

    # --
    # ...
    # --

    def __call__(self) -> str:
        pass

    # --
    # ...
    # --

    def read_image_file(self, image_directory_model: ImageDirectoryModel) -> list[ImageDataModel]:
        try:
            image_data_models = []

            images_folder_adress = Path(image_directory_model.images_folder_adress)

            extensions = {".jpg", ".jpeg", ".png", ".webp"}

            for image_path in images_folder_adress.iterdir():
                if image_path.suffix.lower() not in extensions:
                    continue

                cache = self.cache.get_from_cache(cache_file=self.cache_file_name, is_change_k_v=True)
                if cache:
                    if cache.get(str(image_path)):
                        continue

                image_data_model = ImageDataModel(images_address=f"{images_folder_adress}/{image_path.name}", image_name=image_path.name)

                image_data_model.image_data = Image.open(f"{image_data_model.images_address}").convert("RGB")

                image_data_models.append(image_data_model)

            return image_data_models

        except Exception as exp:
            print(f"read_image_file: {exp}")

    # --
    # ...
    # --

    def add_padding_crop_image(self, image_data_model: ImageDataModel, padding=30) -> ImageDataModel:
        try:
            x1, y1, x2, y2 = image_data_model.product_box

            width, height = image_data_model.image_data.size

            x1 = max(0, x1 - padding)
            y1 = max(0, y1 - padding)
            x2 = min(width, x2 + padding)
            y2 = min(height, y2 + padding)

            image_box = x1, y1, x2, y2
            image_data_model.image_data = image_data_model.image_data.crop(image_box)

            image_data_model.mask = image_data_model.mask[y1:y2, x1:x2]

            return image_data_model

        except Exception as exp:
            print(f"add_padding_crop_image: {exp}")
