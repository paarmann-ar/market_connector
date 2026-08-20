from apis.wordpress_api.config.wordpress_api_config import (
    WordpressApiConfig,
)
from apis.wordpress_api.core.base_wordpress_api import BaseWordpressApi
from apis.wordpress_api.models.wordpress_media_model import WordpressMediaModel
from apis.wordpress_api.services.wordpress_media import WordpressMedia
from apis.wordpress_api.services.wordpress_users import WordpressUsers

# --
# ...
# --


class WordpressApi(BaseWordpressApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.wordpress_media = WordpressMedia()
        self.wordpress_users = WordpressUsers()
        self.wordpress_media_model = WordpressMediaModel

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return WordpressApiConfig().get_dictionary()

    # --
    # ...
    # --

    def upload_media_models_from_disk(self, media_models: list[WordpressMediaModel]) -> str:

        try:
            source_urls = []
            for media_model in media_models:
                source_urls.append(self.wordpress_media.upload_media_model(media_model=media_model))

                self.prompt_on_screen(f"uploaded media: {media_model}")

            return source_urls

        except Exception as exp:
            self.error(f"upload_media_models: {exp}")

    # --
    # ...
    # --

    def get_wordpress_media_models_by_name(self, media_model_names: list[str]) -> list[WordpressMediaModel]:

        try:
            returned_media_models: list[WordpressMediaModel] = []

            for media_model_name in media_model_names:
                media_model = WordpressMediaModel()
                media_model.media_name = media_model_name

                returned_media_models.append(self.wordpress_media.get_wordpress_media_model_by_medial_model_name(media_model=media_model))

            return returned_media_models

        except Exception as exp:
            self.error(f"get_wordpress_media_models_by_name: {exp}")

    # --
    # ...
    # --

    def delete_media_models(self, media_model_names: list[str]) -> str:

        try:
            medial_models_to_delete = self.get_wordpress_media_models_by_name(media_model_names=media_model_names)

            for medial_model_to_delete in medial_models_to_delete:
                self.wordpress_media.delete_wordpress_media_by_media_model(media_model=medial_model_to_delete)

            return

        except Exception as exp:
            self.error(f"delete_media_models: {exp}")


# --
# ...
# --


def test_class():
    media_models: list[str] = []
    media_models.append("nivotemp_63K-WHG.jpg")
    m = WordpressApi().get_wordpress_media_models_by_name(media_model_names=media_models)

    media_model = WordpressMediaModel()
    media_model.media_name = "test.jpg"
    media_model.media_address = "/Users/bpm2/projects/paarmann-ara/test.jpg"
    media_model.wp_alt_text = media_model.media_name
    media_model.wp_title = media_model.media_name
    media_model.wp_caption = media_model.media_name
    media_model.wp_description = media_model.media_name

    media_models_list: list[WordpressMediaModel] = [media_model]
    media_models_name_list: list = [media_model.media_name]

    WordpressApi().upload_media_models(media_models=media_models_list)
    WordpressApi().delete_media_models(media_model_names=media_models_name_list)
