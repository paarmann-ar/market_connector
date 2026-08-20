from apis.ebay_api.models.search_in_ebay_model import SearchInEbayModel
from app.controller.market_connector_controller import MarketConnectorController
from app.controller.setup_market_connector_controller import SetupMarketConnectorController
from market_services.image_services.models.image_directory_model import ImageDirectoryModel

# --
# ...
# --


# product: RM1XA1011 - TÉLÉMÉCANIQUE RM1XA1011 Zubehör Neu
# search_in_ebay_model = SearchInEbayModel(
#     category_name_candidate="Business & Industrie",
#     conditions="{NEW}",
#     deliveryCountry="DE",
#     q="RM1-XA",
#     item_to_fetch=10,
# )

search_in_ebay_models = [
    # SearchInEbayModel(
    # #     category_name_candidate="Business & Industrie",
    #     conditions="{NEW}",
    #     deliveryCountry="DE",
    #     q="Axis Q6135-LE PTZ",
    #     item_to_fetch=1,
    #     price_anpassen=1,
    #     target_category_name_in_woocommerce="Sensoren"
    # ),
    SearchInEbayModel(
        conditions="{NEW}",
        marketplace="EBAY_US",
        deliveryCountry="US",
        q="FITOK",
        filter="sellers:{jlb_the_farm},price:[..500]",
        item_to_fetch=1,
        price_anpassen=1.5,
    )
]


def reduce_image_size():
    SetupMarketConnectorController().image_provider.image_processing_pipeline.reduce_image_size(ImageDirectoryModel())


def setup():
    SetupMarketConnectorController().register_user_token()


def start():
    for search_in_ebay_model in search_in_ebay_models:
        print(search_in_ebay_model.q)
        MarketConnectorController.sync_ebay_to_woocommerce(search_in_ebay_model=search_in_ebay_model)
        # MarketConnectorController.create_ebay_offers(search_in_ebay_model=search_in_ebay_model)


start()
