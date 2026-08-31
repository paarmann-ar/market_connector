from typing import Any

from apis.ebay_api.config.ebay_api_config import (
    EbayApiConfig,
)
from apis.ebay_api.core.base_ebay_api import BaseEbayApi

# --
# ...
# --


class EbayVerkaufPolicys(BaseEbayApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.marketplace_id = self.config_dictionary.get("marketplace_id")
        self.marketplace = self.config_dictionary.get("marketplace")

        self.ebay_account_policy = self.config_dictionary.get("ebay_account_policy")
        self.account_fulfillment_policy = self.config_dictionary.get("account_fulfillment_policy")
        self.account_payment_policy = self.config_dictionary.get("account_payment_policy")
        self.account_return_policy = self.config_dictionary.get("account_return_policy")

        self.products = {}

        self.ebay_token_api = kwargs.get("ebay_token_api", None)

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    #  --
    #  ...
    #  --

    @classmethod
    def get_config_dictionary(cls):
        return EbayApiConfig().get_dictionary()

    #  --
    #  ...
    #  --

    def get_all_fulfillment_policy_on_ebay(self, marketplace_id: str = "") -> Any:

        try:
            if marketplace_id == "":
                marketplace_id = self.marketplace_id

            self.ebay_token_api.get_user_token()
            ebay_access_token = self.ebay_token_api.ebay_user_token

            response = self.request(
                method="get",
                url=f"{self.ebay_account_policy}{self.account_fulfillment_policy}",
                headers={
                    "Authorization": f"Bearer {ebay_access_token}",
                    "X-EBAY-C-MARKETPLACE-ID": f"{marketplace_id}",
                    "Content-Language": "de-DE",
                },
                params={
                    "marketplace_id": marketplace_id,
                },
            )

            self.prompt_on_screen(f"get_all_fulfillment_policy_on_ebay: {response.get('total')}")

            return response.get("fulfillmentPolicies")

        except Exception as exp:
            self.prompt_on_screen(f"get_allskus_on_ebay: {exp}")

    #  --
    #  ...
    #  --

    def get_all_zahlungs_policy_on_ebay(self, marketplace_id: str = "") -> Any:

        try:
            if marketplace_id == "":
                marketplace_id = self.marketplace_id

            self.ebay_token_api.get_user_token()
            ebay_access_token = self.ebay_token_api.ebay_user_token

            response = self.request(
                method="get",
                url=f"{self.ebay_account_policy}{self.account_payment_policy}",
                headers={
                    "Authorization": f"Bearer {ebay_access_token}",
                    "X-EBAY-C-MARKETPLACE-ID": f"{marketplace_id}",
                    "Content-Language": "de-DE",
                },
                params={
                    "marketplace_id": marketplace_id,
                },
            )

            self.prompt_on_screen(f"get_all_zahlung_policy_on_ebay: {response.get('total')}")

            return response.get("paymentPolicies")

        except Exception as exp:
            self.prompt_on_screen(f"get_all_zahlung_policy_on_ebay: {exp}")

    #  --
    #  ...
    #  --

    def get_all_ruckgabes_policy_on_ebay(self, marketplace_id: str = "") -> Any:

        try:
            if marketplace_id == "":
                marketplace_id = self.marketplace_id

            self.ebay_token_api.get_user_token()
            ebay_access_token = self.ebay_token_api.ebay_user_token

            response = self.request(
                method="get",
                url=f"{self.ebay_account_policy}{self.account_return_policy}",
                headers={
                    "Authorization": f"Bearer {ebay_access_token}",
                    "X-EBAY-C-MARKETPLACE-ID": f"{marketplace_id}",
                    "Content-Language": "de-DE",
                },
                params={
                    "marketplace_id": marketplace_id,
                },
            )

            self.prompt_on_screen(f"get_all_ruckgabe_policy_on_ebay: {response.get('total')}")

            return response.get("returnPolicies")

        except Exception as exp:
            self.prompt_on_screen(f"get_all_ruckgabe_policy_on_ebay: {exp}")
