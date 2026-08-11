from image_services.core.base import Base
from image_services.background_operation.config.background_operation_config import BackgroundOperationConfig
from image_services.models.image_data_model import ImageDataModel
from image_services.models.image_directory_model import ImageDirectoryModel
from image_services.core.base import Base
from pathlib import Path
from rembg import remove
from PIL import Image

# --
# ...
# --


class PrepaerImageFile(Base):
    def __init__(self, **kwargs):
        super(**kwargs).__init__(**kwargs)

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

            input_folder = Path(image_directory_model.input_folder_image_adress)
            output_folder = Path(image_directory_model.output_folder_image_adress)

            extensions = {".jpg", ".jpeg", ".png", ".webp"}

            for image_path in input_folder.iterdir():
                if image_path.suffix.lower() not in extensions:
                    continue

                image_data_model = ImageDataModel(
                    input_image_adress=f"{input_folder}/{image_path.name}", output_image_adress=f"{output_folder}/{image_path.name}"
                )

                image_data_model.image_data = Image.open(f"{image_data_model.input_image_adress}").convert("RGB")

                image_data_models.append(image_data_model)

            return image_data_models

        except Exception as exp:
            print(f"read_image_file: {exp}")

    # --
    # ...
    # --

    def add_padding_corp_image(self, image_data_model: ImageDataModel, padding=30) -> ImageDataModel:
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
            print(f"add_padding_corp_image: {exp}")
