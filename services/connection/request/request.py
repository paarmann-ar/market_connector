import sys
import time

import colorama
import requests

import CONSTS
from services.connection.core.base_connection import BaseConnection
from services.connection.request.config.request_config import RequestConfig

# --
# ...
# --


class Request(BaseConnection):
    def __init__(self, **kwargs) -> None:

        try:
            is_use_default_headers = kwargs.get("is_use_default_headers", True)

            if is_use_default_headers:
                self.headers = {
                    "Content-Type": "application/json",
                    "Cache-Control": "no-cache",
                    "Accept": "*/*",
                    "Connection": "keep-alive",
                }

            self.url = kwargs.get("url", None)
            self.headers.update(kwargs.get("headers", {}))
            self.params = kwargs.get("params")
            self.data = kwargs.get("data", None)
            self.json = kwargs.get("json", None)
            self.files = kwargs.get("files")
            self.auth = kwargs.get("auth")
            self.method = kwargs.get("method", "get")
            self.is_download_file = kwargs.get("is_download_file", False)
            self.is_response_json = kwargs.get("is_response_json", True)

        except Exception as exp:
            self.error(f"{__file__}--->{__name__}: {exp!s}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return RequestConfig().instance.dictionary

    # --
    # ...
    # --

    def __call__(self, **kwargs) -> str:
        colorama.init()

        self.headers.clear()

        is_use_default_headers = kwargs.get("is_use_default_headers", True)

        if is_use_default_headers:
            self.headers = {
                "Content-Type": "application/json",
                "Cache-Control": "no-cache",
                "Accept": "*/*",
                "Connection": "keep-alive",
            }

        self.url = kwargs.get("url", None)
        self.headers.update(kwargs.get("headers", {}))
        self.params = kwargs.get("params", None)
        self.data = kwargs.get("data", None)
        self.json = kwargs.get("json", None)
        self.files = kwargs.get("files")
        self.auth = kwargs.get("auth", None)
        self.verify = kwargs.get("verify", True)
        self.timeout = kwargs.get("timeout", (11, 11))
        self.method = kwargs.get("method", "get")
        self.is_response_json = kwargs.get("is_response_json", True)
        self.is_download_file = kwargs.get("is_download_file", False)
        self.download_file_address = kwargs.get("download_file_address", "1.txt")

        self.request_package = {
            "url": self.url,
            "auth": self.auth,
            "headers": self.headers,
            "params": self.params,
            "data": self.data,
            "json": self.json,
            "files": self.files,
            "verify": self.verify,
            "timeout": self.timeout,
        }

        self.delay = kwargs.get("delay", 0.5)
        return self.get_response()

    # --
    # ...
    # --

    async def get_response(self): ...

    def get_response(self, wait_counter=5):

        try:
            sys.set_int_max_str_digits(0)

            response = None

            match self.method.lower():
                case "get":
                    response = requests.get(**self.request_package)

                case "post":
                    response = requests.post(**self.request_package)

                case "patch":
                    response = requests.patch(**self.request_package)

                case "delete":
                    response = requests.delete(**self.request_package)

                case "put":
                    response = requests.put(**self.request_package)

            while response is None and wait_counter > 0:
                time.sleep(self.delay)
                wait_counter -= 1

            if response is None:
                message = f"response is None on {self.method} methode with\n\npayload:\n{self.request_package}"

                print(message)

                raise ValueError(message)

            if response.status_code == 401:
                print(
                    "The current user is not correctly authenticated or the session or authentication token has expired."
                )
                return "expired token"

            response = (
                response
                if response.status_code in [204, 200, 201]
                else print(
                    f"{CONSTS.COLORS.AQUA_PROMPT.value}{response.text}{CONSTS.COLORS.ENDC.value}"
                )
            )

            if response.status_code == 204:
                return True

            elif self.is_response_json and response:
                response = response.json()

            elif self.is_download_file and response:
                with open(self.download_file_address, "wb") as file_to_download:
                    file_to_download.write(response.content)

            return response

        except ValueError as v_exp:
            print(f"{v_exp}")

            print(f"{CONSTS.COLORS.AQUA_PROMPT.value}{response.text}{CONSTS.COLORS.ENDC.value}")

        except AttributeError as a_exp:
            print(f"{CONSTS.COLORS.AQUA_PROMPT.value}{a_exp}{CONSTS.COLORS.ENDC.value}")

        except Exception as exp:
            print(f"{exp}")
