from apis.wordpress_api.config.wordpress_api_config import (
    WordpressApiConfig,
)
from apis.wordpress_api.core.base_wordpress_api import BaseWordpressApi
from apis.wordpress_api.models.wordpress_media_model import WordpressMediaModel

# --
# ...
# --


class WordpressMedia(BaseWordpressApi):
    def __init__(self, **kwargs) -> None:
        self.base_url = self.instance.config_dictionary.get("base_url")
        self.media_url = self.instance.config_dictionary.get("media_url")

        self.wp_user = self.instance.config_dictionary.get("wp_user")
        self.wp_application_password = self.instance.config_dictionary.get(
            "wp_application_password"
        )
        self.wp_password = self.instance.config_dictionary.get("wp_password")

        self.media_dict = {}

        self.prompt_on_screen(f"{__class__.__name__}, {id(__class__)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return WordpressApiConfig().instance.dictionary

    # --
    # ...
    # --

    def upload_media_model(self, media_model: WordpressMediaModel):

        try:
            media_file = {"file": open(media_model.media_address, "rb")}

            data = {
                "title": media_model.wp_title,
                "caption": media_model.wp_caption,
                "description": media_model.wp_description,
                "alt_text": media_model.wp_alt_text,
                "slug": media_model.wp_slug,
            }

            response = self.request(
                is_use_default_headers=False,
                method="post",
                url=f"{self.base_url}/{self.media_url}",
                headers={"Content-Disposition": f"attachment; filename={media_model.media_name}"},
                files=media_file,
                data=data,
                auth=(self.wp_user, self.wp_application_password),
            )

            self.prompt_on_screen(f"upload_media_model: {response}")

            return True

        except Exception as exp:
            print(f"upload_media_model: {exp}")

    # --
    # ...
    # --

    def upload_media_from_url(self, media_url: str):

        try:
            pass

        except Exception as exp:
            print(f"upload_media_model_from_url: {exp}")

    # --
    # ...
    # --

    def get_wordpress_media_model_by_medial_model_name(
        self, media_model: WordpressMediaModel
    ) -> WordpressMediaModel:

        try:
            response = self.request(
                method="get",
                url=f"{self.base_url}/{self.media_url}",
                auth=(self.wp_user, self.wp_application_password),
                params={"search": media_model.media_name},
            )

            returned_media_model = WordpressMediaModel()

            returned_media_model.media_name = media_model.media_name
            returned_media_model.media_address = media_model.media_address
            returned_media_model.wp_id = response[0]["id"]
            returned_media_model.wp_url = response[0]["source_url"]
            returned_media_model.wp_date = response[0]["date"]
            returned_media_model.wp_title = response[0]["title"]["rendered"]
            returned_media_model.wp_caption = response[0]["caption"]["rendered"]
            returned_media_model.wp_description = response[0]["description"]["rendered"]
            returned_media_model.wp_alt_text = response[0]["alt_text"]
            returned_media_model.wp_slug = response[0]["slug"]
            returned_media_model.wp_post = response[0]["post"]
            returned_media_model.wp_meta = response[0]["meta"]
            returned_media_model.wp_link = response[0]["link"]
            returned_media_model.wp_status = response[0]["status"]

            self.prompt_on_screen(f"returned_media_model: {returned_media_model}")

            return returned_media_model

        except Exception as exp:
            print(f"get_wordpress_media_model_by_medial_model_name: {exp}")

    # --
    # ...
    # --

    def delete_wordpress_media_by_media_model(self, media_model: WordpressMediaModel):

        try:
            response = self.request(
                method="delete",
                url=f"{self.base_url}/{self.media_url}/{media_model.wp_id}",
                auth=(self.wp_user, self.wp_application_password),
                params={"force": True},
            )

            self.prompt_on_screen(f"medias has been deleted: {media_model.wp_id}")

            return response

        except Exception as exp:
            print(f"delete_wordpress_media_by_media_model: {exp}")

    # --
    # ...
    # --

    def delete_wordpress_media_by_wp_id(self, wp_id: int):

        try:
            response = self.request(
                method="delete",
                url=f"{self.base_url}/{self.media_url}/{wp_id}",
                auth=(self.wp_user, self.wp_application_password),
                params={"force": True},
            )

            self.prompt_on_screen(f"medias has been deleted: {wp_id}")

            return response

        except Exception as exp:
            print(f"delete_wordpress_media_by_wp_id: {exp}")
