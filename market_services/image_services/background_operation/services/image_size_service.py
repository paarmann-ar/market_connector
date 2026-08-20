from PIL import Image

from market_services.image_services.background_operation.config.background_operation_config import BackgroundOperationConfig
from market_services.image_services.core.base import Base
from market_services.image_services.models.image_data_model import ImageDataModel

# --
# ...
# --


class ImageSizeService(Base):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

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

    def optimize_image(self, image_data_model: ImageDataModel) -> ImageDataModel:

        suffix = image_data_model.image_name.find(".")
        suffix = image_data_model.image_name[suffix:].lower()

        if suffix in {".jpg", ".jpeg"}:
            # Keep RGB/RGBA compatibility for JPEG
            if image_data_model.image_data.mode in ("RGBA", "LA", "P"):
                background = Image.new("RGB", image_data_model.image_data.size, "white")
                if image_data_model.image_data.mode == "P":
                    image_data_model.image_data = image_data_model.image_data.convert("RGBA")
                background.paste(image_data_model.image_data, mask=image_data_model.image_data.getchannel("A"))
                image_data_model.image_data = background
            else:
                image_data_model.image_data = image_data_model.image_data.convert("RGB")
