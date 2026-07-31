from apis.wordpress_api.wordpress_api.core.base_wordpress_api import BaseWordpressApi
from apis.wordpress_api.wordpress_api.config.wordpress_api_config import (
    WordpressApiConfig,
)
import CONSTS

# --
# ...
# --


class WordpressUsers(BaseWordpressApi):
    def __init__(self, **kwargs) -> None:
        self.base_url = self.instance.config_dictionary.get("base_url")
        self.user_url = self.instance.config_dictionary.get("user_url")

        self.wp_user= self.instance.config_dictionary.get("wp_user")
        self.wp_application_password=self.instance.config_dictionary.get("wp_application_password")
        self.wp_password= self.instance.config_dictionary.get("wp_password")

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

    def test_is_valid_user(self):

        try:

            response = self.request(
                method="get",
                url=f"{self.base_url}{self.user_url}",
                auth=(self.wp_user, self.wp_application_password)
            )

            self.prompt_on_screen(
                f"response: {response}"
            )

            return response
        
        except Exception as exp:
            print(f"test_is_valid_user: {exp}")