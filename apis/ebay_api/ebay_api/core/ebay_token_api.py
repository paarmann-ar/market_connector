from apis.ebay_api.ebay_api.core.base_ebay_api import BaseEbayApi
from apis.ebay_api.ebay_api.config.ebay_api_config import (
    EbayApiConfig,
)
import time
import base64

# --
# ...
# --

class EbayTokenApi(BaseEbayApi):
    def __init__(self, **kwargs) -> None:
        self.base_url = self.instance.config_dictionary.get("base_url")
        self.token_url = self.instance.config_dictionary.get("token_url")
        self.client_id = self.instance.config_dictionary.get("client_id")
        self.dev_id = self.instance.config_dictionary.get("dev_id")
        self.client_secret = self.instance.config_dictionary.get("client_secret")

        self.ebay_access_token = None
        self.expires_in_token = 0
        self.expires_get_time = time.time()

        self.prompt_on_screen(f"{__class__.__name__}, {id(__class__)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return EbayApiConfig().instance.dictionary

    # --
    # ...
    # --

    def __call__(self, **kwargs) -> str:
        return self.get_token(**kwargs)

    # --
    # ... tocken
    # --

    def get_token(self, **kwargs):

        try:

            expire_token_in_next_seconds = int(time.time() - self.expires_get_time)

            if self.expires_in_token - 30 > expire_token_in_next_seconds:
                self.prompt_on_screen(
                    f"Token is valid for {self.expires_in_token - expire_token_in_next_seconds} seconds"
                )
                return self.ebay_access_token

            credentials = f"{self.client_id}: {self.client_secret}"
            encoded = base64.b64encode(credentials.encode()).decode()

            data = {
                "grant_type": "client_credentials",
                "scope": "https://api.ebay.com/oauth/api_scope",
            }

            if self.ebay_access_token:
                data["refresh_token"] = self.ebay_access_token

            response = self.request(
                method="post",
                url=f"{self.base_url}{self.token_url}",
                headers={"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Basic {encoded}"},
                data=data,
            )

            self.ebay_access_token = response.get("access_token", None)
            self.expires_in_token = response.get("expires_in", 0)
            self.expires_get_time = time.time()

            self.prompt_on_screen(f"access Token is: {self.ebay_access_token}")

            return self.ebay_access_token

        except Exception as exp:
            print(f"get_token: {exp}")

