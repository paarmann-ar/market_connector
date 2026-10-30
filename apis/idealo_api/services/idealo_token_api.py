import base64
import time
import webbrowser
from urllib.parse import parse_qs, urlencode, urlparse

from apis.idealo_api.config.idealo_api_config import (
    IdealoApiConfig,
)
from apis.idealo_api.core.base_idealo_api import BaseIdealoApi

# --
# ...
# --


class IdealoTokenApi(BaseIdealoApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.idealo_client_id = self.config_dictionary.get("idealo_client_id")
        self.idealo_password = self.config_dictionary.get("idealo_password")

        self.base_url = self.config_dictionary.get("base_url")
        self.oauth_api_url = self.config_dictionary.get("oauth_api_url")

        self.idealo_token = None
        self.expires_token = 0
        self.expires_token_get_time = time.time()

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    #  --
    #  ...
    #  --

    @classmethod
    def get_config_dictionary(cls):
        return IdealoApiConfig().get_dictionary()

    #  --
    #  ...
    #  --

    def __call__(self, **kwargs) -> str:
        pass

    #  --
    #  ... application_token

    #  --

    def get_token(self, **kwargs):

        try:
            expire_token_in_next_seconds = int(time.time() - self.expires_token_get_time)

            if self.expires_token - 30 > expire_token_in_next_seconds:
                self.prompt_on_screen(f"Token is valid for {self.expires_token - expire_token_in_next_seconds} seconds")
                return self.idealo_token

            credentials = f"{self.idealo_client_id}:{self.idealo_password}"
            encoded = base64.b64encode(credentials.encode()).decode()

            data = {
                "grant_type": "client_credentials",
            }

            response = self.request(
                method="post",
                url=f"{self.base_url}{self.oauth_api_url}",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Basic {encoded}",
                },
                data=data,
            )

            self.idealo_token = response.get("access_token", None)
            self.expires_token = response.get("expires_in", 0)
            self.expires_token_get_time = time.time()

            self.prompt_on_screen(f"idealo access Token is: {bool(self.idealo_token)}")

            return self.idealo_token

        except Exception as exp:
            self.prompt_on_screen(f"get_token: {exp}")
