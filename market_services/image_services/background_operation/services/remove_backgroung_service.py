from PIL import Image

from market_services.image_services.background_operation.config.background_operation_config import BackgroundOperationConfig
from market_services.image_services.core.base import Base
from market_services.image_services.models.image_data_model import ImageDataModel

# --
# ...
# --


class RemoveBackgroungService(Base):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    #  --
    #  ...
    #  --

    @classmethod
    def get_config_dictionary(cls):
        return BackgroundOperationConfig().get_dictionary()

    #  --
    #  ...
    #  --

    def __call__(self) -> str:
        pass

    #  --
    #  ...
    #  --

    def make_background_white(self, image_data_model: ImageDataModel) -> ImageDataModel:
        try:
            image = image_data_model.image_data.convert("RGB")
            mask = image_data_model.mask

            mask_image = Image.fromarray(mask).convert("L")

            white_background = Image.new("RGB", image.size, (255, 255, 255))
            result = Image.composite(image, white_background, mask_image)
            image_data_model.image_data = result

            return image_data_model

        except Exception as exp:
            print(f"make_background_white: {exp}")

    #  --
    #  ...
    #  --

    def remove_backgroung_from_photo(self, image_data_model: ImageDataModel) -> ImageDataModel:

        try:
            image = image_data_model.image_data.convert("RGB")

            result = self.remove(image, session=self.session)
            result = result.convert("RGBA")

            white_background = Image.new("RGBA", image.size, (255, 255, 255, 255))

            final_image = Image.alpha_composite(white_background, result)

            final_image = final_image.convert("RGB")

            image_data_model.image_data = final_image

            return image_data_model

        except Exception as exp:
            print(f"remove_backgroung_from_photo: {exp}")

    #  --
    #  ...
    #  --

    def finalize_image(self, image_data_model: ImageDataModel) -> ImageDataModel:
        try:
            image_data_model.image_data.save(
                image_data_model.images_address, "WEBP", quality=100, method=6, optimize=True, progressive=True
            )

            return image_data_model

        except Exception as exp:
            print(f"finalize_image: {exp}")

    #  --
    #  ...
    #  --

    def resize_to_fixed_canvas(
        self,
        image_data_model: ImageDataModel,
        size: tuple[int, int] = (1200, 1200),
    ) -> ImageDataModel:
        try:
            image = image_data_model.image_data.convert("RGB")

            target_width, target_height = size

            #  Keep the original aspect ratio.
            image.thumbnail(
                (target_width, target_height),
                Image.Resampling.LANCZOS,
            )

            #  Create fixed-size white canvas.
            canvas = Image.new(
                "RGB",
                (target_width, target_height),
                (255, 255, 255),
            )

            #  Center image on canvas.
            x = (target_width - image.width) // 2
            y = (target_height - image.height) // 2

            canvas.paste(image, (x, y))

            image_data_model.image_data = canvas

            return image_data_model

        except Exception as exp:
            print(f"resize_to_fixed_canvas: {exp}")
            return None
