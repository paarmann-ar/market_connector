import CONSTS
from image_services.background_operation.config.background_operation_config import BackgroundOperationConfig
from image_services.background_operation.services.find_product_box import FindProductBox
from image_services.background_operation.services.prepaer_image_file import PrepaerImageFile
from image_services.background_operation.services.remove_backgroung_service import RemoveBackgroungService
from image_services.core.base import Base
from image_services.models.image_data_model import ImageDataModel
from image_services.models.image_directory_model import ImageDirectoryModel

# --
# ...
# --


class BackgroundOperation(Base):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        images_address = f"{CONSTS.ROOT_DIR}{self.config_dictionary.get('images_address')}"

        self.image_directory_model = ImageDirectoryModel(images_folder_adress=images_address)
        self.prepaer_image_file = PrepaerImageFile()
        self.find_product_box = FindProductBox()
        self.remove_backgroung_service = RemoveBackgroungService()

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(self):
        return BackgroundOperationConfig().get_dictionary()

    # --
    # ...
    # --

    def remove_set_white_backgroung_on_photo(self, image_directory_model: ImageDirectoryModel = None) -> list[ImageDataModel]:

        try:
            if not image_directory_model:
                image_directory_model = self.image_directory_model

            image_data_models = self.prepaer_image_file.read_image_file(image_directory_model=image_directory_model)

            for image_data_model in image_data_models:
                image_data_model = self.find_product_box.find_product_box(image_data_model=image_data_model)

                image_data_model = self.prepaer_image_file.add_padding_corp_image(image_data_model=image_data_model, padding=30)

                image_data_model = self.remove_backgroung_service.make_background_white(image_data_model)

                image_data_model = self.remove_backgroung_service.finalize_image(image_data_model=image_data_model)

                self.prompt_on_screen(f"image proccing for {image_data_model.images_address} has been finished")

            return image_data_models

        except Exception as exp:
            self.error(f"remove_set_white_backgroung_on_photo: {exp}")

    # --
    # ...
    # --


# x=BackgroundOperation()
# x.remove_set_white_backgroung_on_photo()
