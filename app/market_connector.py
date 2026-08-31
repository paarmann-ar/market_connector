from apis.ebay_api.models.search_in_ebay_model import SearchInEbayModel
from apis.matterhorn_moda_api.models.search_in_matterhorn_moda_model import SearchInMatterhornModaModel
from apis.woocommerce_api.models.search_in_woocommerce_model import SearchInWoocommerceModel
from apis.zalando_lounge_api.models.search_in_zalando_lounge_model import SearchInZalandoLoungeModel
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
search_in_matterhorn_moda_models = [
    SearchInMatterhornModaModel(price_anpassen=2.3, sale_price_anpassen=2, is_remove_description_html=False)
]

search_in_zalando_lounge_models = [SearchInZalandoLoungeModel(campaign_id="ZZO4FTR", sku="ZUN243D04X-K23")]

search_in_woocommerce_models = [SearchInWoocommerceModel(name="Motor Display Rate")]

search_in_ebay_models = [
    SearchInEbayModel(
        legacy_item_id=178354496712,
        #      category_name_candidate="Business & Industrie",
        marketplace="EBAY_FR",
        marketplace_id="EBAY_FR",
        deliveryCountry="FR",
        item_to_fetch=1,
        price_anpassen=1.4,
        target_category_name_in_woocommerce="Sonstige",
    )  # 168430948054 q63
    #  SearchInEbayModel(
    #      legacy_item_id=318647115657,
    #  #     category_name_candidate="Business & Industrie",
    #      marketplace="EBAY_US",
    #      marketplace_id="EBAY_US",
    #      deliveryCountry="US",
    #      item_to_fetch=1,
    #      price_anpassen=1.6,
    #      target_category_name_in_woocommerce="Sonstige",
    #  ),
    #  SearchInEbayModel(
    #      conditions="{NEW}",
    #      marketplace="EBAY_US",
    #      deliveryCountry="US",
    #      q="FITOK",
    #      filter="sellers:{jlb_the_farm},price:[..500]",
    #      item_to_fetch=1,
    #      price_anpassen=1.5,
    #      target_category_name_in_woocommerce="Sonstige",
    #  )
]

# --
# ...
# --


def reduce_image_size():
    SetupMarketConnectorController().image_provider.image_processing_pipeline.reduce_image_size(ImageDirectoryModel())


def white_backgroung():
    SetupMarketConnectorController().image_provider.image_processing_pipeline.white_backgroung(ImageDirectoryModel())


# --
# ...
# --


def setup():
    SetupMarketConnectorController().register_user_token()


# --
# ...
# --


def sync_ebay_to_woocommerce():
    for search_in_ebay_model in search_in_ebay_models:
        print(search_in_ebay_model.q)
        MarketConnectorController.sync_ebay_to_woocommerce(search_in_ebay_model=search_in_ebay_model)


#  MarketConnectorController.create_ebay_offers(search_in_ebay_model=search_in_ebay_model)


def sync_woocommerce_to_ebay():
    for search_in_woocommerce_model in search_in_woocommerce_models:
        MarketConnectorController.sync_woocommerce_to_ebay(search_in_woocommerce_model=search_in_woocommerce_model)


def sync_zalando_lounge_to_woocommerce():
    for search_in_zalando_lounge_model in search_in_zalando_lounge_models:
        k = MarketConnectorController.sync_zalando_lounge_to_woocommerce(search_in_zalando_lounge_model=search_in_zalando_lounge_model)


def sync_matterhorn_moda_to_woocommerce():
    for search_in_matterhorn_moda_model in search_in_matterhorn_moda_models:
        MarketConnectorController.sync_matterhorn_moda_to_woocommerce(search_in_matterhorn_moda_model=search_in_matterhorn_moda_model)


sync_matterhorn_moda_to_woocommerce()
