import base64
import time
import webbrowser
from urllib.parse import parse_qs, urlencode, urlparse

from apis.ebay_api.config.ebay_api_config import (
    EbayApiConfig,
)
from apis.ebay_api.core.base_ebay_api import BaseEbayApi

# --
# ...
# --


class EbayTokenApi(BaseEbayApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.ebay_identity_oauth_api = self.config_dictionary.get("ebay_identity_oauth_api")
        self.register_scope = self.config_dictionary.get("register_scope")

        self.client_id = self.config_dictionary.get("client_id")
        self.dev_id = self.config_dictionary.get("dev_id")
        self.client_secret = self.config_dictionary.get("client_secret")
        self.redirect_uri = self.config_dictionary.get("redirect_uri")
        self.scope = self.config_dictionary.get("scope")
        self.auth_url = self.config_dictionary.get("auth_url")
        self.refresh_token = self.config_dictionary.get("refresh_token")

        self.ebay_application_token = None
        self.expires_application_token = 0
        self.expires_application_token_get_time = time.time()

        self.ebay_user_token = None
        self.expires_user_token = 0
        self.expires_user_token_get_time = time.time()

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return EbayApiConfig().get_dictionary()

    # --
    # ...
    # --

    def __call__(self, **kwargs) -> str:
        pass

    # --
    # ... application_token

    # --

    def get_application_token(self, **kwargs):

        try:
            expire_token_in_next_seconds = int(time.time() - self.expires_application_token_get_time)

            if self.expires_application_token - 30 > expire_token_in_next_seconds:
                self.prompt_on_screen(f"Token is valid for {self.expires_application_token - expire_token_in_next_seconds} seconds")
                return self.ebay_application_token

            credentials = f"{self.client_id}:{self.client_secret}"
            encoded = base64.b64encode(credentials.encode()).decode()

            data = {
                "grant_type": "client_credentials",
                "scope": self.scope,
            }

            response = self.request(
                method="post",
                url=f"{self.ebay_identity_oauth_api}",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Basic {encoded}",
                },
                data=data,
            )

            self.ebay_application_token = response.get("access_token", None)
            self.expires_application_token = response.get("expires_in", 0)
            self.expires_application_token_get_time = time.time()

            self.prompt_on_screen(f"access Token is: {bool(self.ebay_application_token)}")

            return self.ebay_application_token

        except Exception as exp:
            self.prompt_on_screen(f"get_application_token: {exp}")

    # --
    # ... get_user_token baray upload kardan monteha in refresh dare
    # --

    def get_user_token(self, **kwargs):

        try:
            expire_token_in_next_seconds = int(time.time() - self.expires_user_token_get_time)

            if self.expires_user_token - 30 > expire_token_in_next_seconds:
                self.prompt_on_screen(f"User token is valid for {self.expires_user_token - expire_token_in_next_seconds} seconds")
                return self.ebay_user_token

            credentials = f"{self.client_id}:{self.client_secret}"
            encoded = base64.b64encode(credentials.encode()).decode()

            data = {
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
            }

            response = self.request(
                method="post",
                url=f"{self.ebay_identity_oauth_api}",
                headers={
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Authorization": f"Basic {encoded}",
                },
                data=data,
            )

            self.ebay_user_token = response.get("access_token")
            self.expires_user_token = response.get("expires_in", 0)
            self.expires_user_token_get_time = time.time()

            self.prompt_on_screen(f"user access Token is: {bool(self.ebay_user_token)}")

            return self.ebay_user_token

        except Exception as exp:
            self.prompt_on_screen(f"get_user_token: {exp}")

    # --
    # ... register_user_token baray upload kardan bayad register anjam beshe bad miche get_user_token estefadeh kard
    # --

    def register_user_token(self, **kwargs):

        params = {"client_id": self.client_id, "response_type": "code", "redirect_uri": self.redirect_uri, "scope": self.register_scope}
        auth_url = self.auth_url + urlencode(params)
        print(f"auth_url: {auth_url}")
        webbrowser.open(auth_url)

        callback_url = input("Paste callback URL: ")

        query = parse_qs(urlparse(callback_url).query)
        code = query["code"][0]

        print(f"Authorization code received:{code}")

        credentials = f"{self.client_id}:{self.client_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()

        response = self.request(
            method="post",
            url=f"{self.ebay_identity_oauth_api}",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": f"Basic {encoded}",
            },
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.redirect_uri,
            },
        )

        self.prompt_on_screen(f"access_token: {response.get('access_token')}\nrefresh_token:{response.get('refresh_token')}")
