from apis.wordpress_api.config.wordpress_api_config import (
    WordpressApiConfig,
)
from apis.wordpress_api.core.base_wordpress_api import BaseWordpressApi

# --
# ...
# --


class WordpressUsers(BaseWordpressApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.base_url = self.config_dictionary.get("base_url")
        self.user_url = self.config_dictionary.get("user_url")

        self.wp_user = self.config_dictionary.get("wp_user")
        self.wp_application_password = self.config_dictionary.get("wp_application_password")
        self.wp_password = self.config_dictionary.get("wp_password")

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    #  --
    #  ...
    #  --

    @classmethod
    def get_config_dictionary(cls):
        return WordpressApiConfig().get_dictionary()

    #  --
    #  ...
    #  --

    def test_is_valid_user(self):

        try:
            response = self.request(
                method="get",
                url=f"{self.base_url}{self.user_url}",
                auth=(self.wp_user, self.wp_application_password),
            )

            self.prompt_on_screen(f"response: {response}")

            return response

        except Exception as exp:
            self.error(f"test_is_valid_user: {exp}")
