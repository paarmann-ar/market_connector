from image_services.core.base import Base
from image_services.remove_background.config.remove_background_config import RemoveBackgroundConfig
from image_services.remove_background.services.remove_backgroung_service import RemoveBackgroungService
from image_services.remove_background.models.image_data_model import ImageDataModel
from image_services.remove_background.models.image_directory_model import ImageDirectoryModel
from image_services.remove_background.services.prepaer_image_file import PrepaerImageFile
from image_services.remove_background.services.find_product_box import FindProductBox
import CONSTS

# --
# ...
# --


class RemoveBackground(Base):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        input_folder = f"{CONSTS.ROOT_DIR}{self.config_dictionary.get('input_folder')}"
        output_folder = f"{CONSTS.ROOT_DIR}{self.config_dictionary.get('output_folder')}"

        self.image_directory_model = ImageDirectoryModel(input_folder_image_adress=input_folder, output_folder_image_adress=output_folder)
        self.prepaer_image_file = PrepaerImageFile()
        self.find_product_box = FindProductBox()
        self.remove_backgroung_service = RemoveBackgroungService()

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(self):
        return RemoveBackgroundConfig().get_dictionary()

    # --
    # ...
    # --

    def remove_backgroung_from_photo(self) -> bool:

        try:
            image_data_models = self.prepaer_image_file.read_image_file(image_directory_model=self.image_directory_model)

            for image_data_model in image_data_models:
                self.find_product_box.find_product_box(image_data_model=image_data_model)

                image_data_model = self.prepaer_image_file.add_padding_corp_image(image_data_model=image_data_model, padding=30)

                self.remove_backgroung_service.finalize_image(image_data_model=image_data_model)

                self.prompt_on_screen(f"image has been finished at: {image_data_model.output_image_adress}")

                #image_data_model = self.remove_backgroung_service.make_background_white(image_data_model)

            return True

        except Exception as exp:
            self.error(f"remove_backgroung_from_photo: {exp}")

    # --
    # ...
    # --


RemoveBackground().remove_backgroung_from_photo()
