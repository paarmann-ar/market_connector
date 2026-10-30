from apis.idealo_api.config.idealo_api_config import (
    IdealoApiConfig,
)
from apis.idealo_api.core.base_idealo_api import BaseIdealoApi
from apis.idealo_api.services.idealo_token_api import IdealoTokenApi
from apis.idealo_api.services.idealo_partner_web_service import IdealoPartnerWebService
from apis.idealo_api.models.idealo_offer_model import IdealoOfferModel

# --
# ...
# --


class IdealoApi(BaseIdealoApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.idealo_token_api = IdealoTokenApi()
        self.idealo_partner_web_service = IdealoPartnerWebService(idealo_token_api=self.idealo_token_api)

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

    def pipeline_create_offer_on_idealo(self, idealo_offer_model: IdealoOfferModel):
        self.prompt_on_screen(f"upload: {idealo_offer_model.title}")
        self.idealo_partner_web_service.put_idealo_offer(idealo_offer_model=idealo_offer_model)

    #  --
    #  ...
    #  --

    def get_offer_on_idealo(self, idealo_offer_model: IdealoOfferModel):
        self.prompt_on_screen(f"download: {idealo_offer_model.title}")
        idealo_offer_model = self.idealo_partner_web_service.get_idealo_offer(idealo_offer_model=idealo_offer_model)
        self.prompt_on_screen(idealo_offer_model)

    #  --
    #  ...
    #  --

    def update_offer_on_idealo(self, idealo_offer_model: IdealoOfferModel):
        del_attr = ["replica", "used", "download", "delivery_costs", "payment_costs"]

        for attr in del_attr:
            idealo_offer_model.__delattr__(attr)

        self.prompt_on_screen(f"update: {idealo_offer_model.title}")
        self.idealo_partner_web_service.update_idealo_offer(idealo_offer_model=idealo_offer_model)

    #  --
    #  ...
    #  --

    def delete_offer_on_idealo(self, idealo_offer_model: IdealoOfferModel):
        self.prompt_on_screen(f"delete: {idealo_offer_model.title}")
        idealo_offer_model = self.idealo_partner_web_service.delete_idealo_offer(idealo_offer_model=idealo_offer_model)


    #  --
    #  ...
    #  --

    def delete_all_offer_on_idealo(self):
        self.prompt_on_screen(f"delete all offers")
        self.idealo_partner_web_service.delete_all_idealo_offer()
