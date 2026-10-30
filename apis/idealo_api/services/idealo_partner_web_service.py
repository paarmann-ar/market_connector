from typing import Any

from apis.idealo_api.config.idealo_api_config import IdealoApiConfig
from apis.idealo_api.core.base_idealo_api import BaseIdealoApi
from apis.idealo_api.models.idealo_offer_model import IdealoOfferModel

# --
# ...
# --


class IdealoPartnerWebService(BaseIdealoApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.idealo_token_api = kwargs.get("idealo_token_api", None)

        self.base_partner_web_service_url = self.config_dictionary.get("base_partner_web_service_url", None)
        self.partner_web_service_url = self.config_dictionary.get("partner_web_service_url", None)
        self.shop_id = self.config_dictionary.get("shop_id", None)

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

    def put_idealo_offer(self, idealo_offer_model: IdealoOfferModel) -> Any:

        try:
            self.idealo_token_api.get_token()

            json = idealo_offer_model.to_dict()

            response = self.request(
                method="put",
                url=f"{self.base_partner_web_service_url}{self.partner_web_service_url}/{self.shop_id}/offer/{idealo_offer_model.sku}",
                headers={
                    "Authorization": f"Bearer {self.idealo_token_api.idealo_token}",
                    "Content-Type": "application/json",
                },
                json=json,
            )

            self.prompt_on_screen(f"put_idealo_offer: {response}")

            return response

        except Exception as exp:
            self.prompt_on_screen(f"put_idealo_offer: {exp}")

    #  --
    #  ...
    #  --

    def get_idealo_offer(self, idealo_offer_model: IdealoOfferModel) -> IdealoOfferModel:

        try:
            self.idealo_token_api.get_token()

            json = idealo_offer_model.to_dict()

            response = self.request(
                method="get",
                url=f"{self.base_partner_web_service_url}{self.partner_web_service_url}/{self.shop_id}/offer/{idealo_offer_model.sku}",
                headers={
                    "Authorization": f"Bearer {self.idealo_token_api.idealo_token}",
                    "Content-Type": "application/json",
                },
                json=json,
            )

            self.prompt_on_screen(f"get_idealo_offer: {response.get('title')}")

            return IdealoOfferModel(**response)

        except Exception as exp:
            self.prompt_on_screen(f"get_idealo_offer: {exp}")

    #  --
    #  ...
    #  --

    def update_idealo_offer(self, idealo_offer_model: IdealoOfferModel) -> IdealoOfferModel:

        try:
            self.idealo_token_api.get_token()

            json = idealo_offer_model.to_dict()

            response = self.request(
                method="patch",
                url=f"{self.base_partner_web_service_url}{self.partner_web_service_url}/{self.shop_id}/offer/{idealo_offer_model.sku}",
                headers={
                    "Authorization": f"Bearer {self.idealo_token_api.idealo_token}",
                    "Content-Type": "application/json",
                },
                json=json,
            )

            self.prompt_on_screen(f"update_idealo_offer: {response}")

            return response

        except Exception as exp:
            self.prompt_on_screen(f"update_idealo_offer: {exp}")

    #  --
    #  ...
    #  --

    def delete_idealo_offer(self, idealo_offer_model: IdealoOfferModel) -> IdealoOfferModel:

        try:
            self.idealo_token_api.get_token()

            json = idealo_offer_model.to_dict()

            response = self.request(
                method="delete",
                url=f"{self.base_partner_web_service_url}{self.partner_web_service_url}/{self.shop_id}/offer/{idealo_offer_model.sku}",
                headers={
                    "Authorization": f"Bearer {self.idealo_token_api.idealo_token}",
                    "Content-Type": "application/json",
                },
                json=json,
            )

            self.prompt_on_screen(f"delete_idealo_offer: {response}")

            return response

        except Exception as exp:
            self.prompt_on_screen(f"delete_idealo_offer: {exp}")

    #  --
    #  ...
    #  --

    def delete_all_idealo_offer(self) -> any:

        try:
            self.idealo_token_api.get_token()

            response = self.request(
                method="delete",
                url=f"{self.base_partner_web_service_url}{self.partner_web_service_url}/{self.shop_id}/offer",
                headers={
                    "Authorization": f"Bearer {self.idealo_token_api.idealo_token}",
                    "Content-Type": "application/json",
                },
            )

            self.prompt_on_screen(f"delete_all_idealo_offer: {response}")

            return response

        except Exception as exp:
            self.prompt_on_screen(f"delete_all_idealo_offer: {exp}")
