
from apis.models.fetch_config_model import FetchConfigModel
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
fetch_matterhorn_moda_config_models = [
    FetchConfigModel(
        price_anpassen=2.3,
        sale_price_anpassen=2,
        is_remove_description_html=False,
        attribute_name="Size",
        item_to_fetch=100
    )
]

search_in_zalando_lounge_models = [FetchConfigModel(campaign_id="ZZO4FTR", sku="ZUN243D04X-K23")]

search_in_woocommerce_models = [FetchConfigModel(name="Motor Display Rate")]

search_in_ebay_models = [
    # SearchInEbayModel(
    #     legacy_item_id=178354496712,
    #     #      category_name_candidate="Business & Industrie",
    #     marketplace="EBAY_FR",
    #     marketplace_id="EBAY_FR",
    #     deliveryCountry="FR",
    #     item_to_fetch=1,
    #     price_anpassen=1.4,
    #     target_category_name_in_woocommerce="Sonstige",
    # ),

    # 168430948054 q63
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
    
        FetchConfigModel(
        legacy_item_id=377407787143,
        marketplace="EBAY_DE",
        marketplace_id="EBAY_DE",
        deliveryCountry="DE",
        item_to_fetch=1,
        price_anpassen=1,
        sale_price_anpassen=0.93,
        is_use_image_service=False,
        target_category_name_in_woocommerce="Sonstige"
        
    ),
    # FetchConfigModel(
    #     legacy_item_id=377494651062,
    #     legacy_variation_id=645799670839,
    #     marketplace="EBAY_DE",
    #     marketplace_id="EBAY_DE",
    #     deliveryCountry="DE",
    #     item_to_fetch=1,
    #     price_anpassen=1,
    #     sale_price_anpassen=0.8,
    #     is_use_image_service=False,
    #     target_category_name_in_woocommerce="Sonstige"
    # ),
    # FetchConfigModel(
    #     legacy_item_id=377494651062,
    #     legacy_variation_id=645799670840,
    #     marketplace="EBAY_DE",
    #     marketplace_id="EBAY_DE",
    #     deliveryCountry="DE",
    #     item_to_fetch=1,
    #     price_anpassen=1,
    #     sale_price_anpassen=0.8,
    #     is_use_image_service=False,
    #     target_category_name_in_woocommerce="Sonstige"
    # ),
    # FetchConfigModel(
    #     legacy_item_id=377494651062,
    #     legacy_variation_id=645799670841,
    #     marketplace="EBAY_DE",
    #     marketplace_id="EBAY_DE",
    #     deliveryCountry="DE",
    #     item_to_fetch=1,
    #     price_anpassen=1,
    #     sale_price_anpassen=0.8,
    #     is_use_image_service=False,
    #     target_category_name_in_woocommerce="Sonstige"
    # ),
    # FetchConfigModel(
    #     legacy_item_id=377494651062,
    #     legacy_variation_id=645799670843,
    #     marketplace="EBAY_DE",
    #     marketplace_id="EBAY_DE",
    #     deliveryCountry="DE",
    #     item_to_fetch=1,
    #     price_anpassen=1,
    #     sale_price_anpassen=0.8,
    #     is_use_image_service=False,
    #     target_category_name_in_woocommerce="Sonstige"
    # ),
    # FetchConfigModel(
    #     legacy_item_id=377494651062,
    #     legacy_variation_id=645799670842,
    #     marketplace="EBAY_DE",
    #     marketplace_id="EBAY_DE",
    #     deliveryCountry="DE",
    #     item_to_fetch=1,
    #     price_anpassen=1,
    #     sale_price_anpassen=0.8,
    #     is_use_image_service=False,
    #     target_category_name_in_woocommerce="Sonstige"
    # ),
    # FetchConfigModel(
    #     legacy_item_id=377494682430,
    #     legacy_variation_id=645800639897,
    #     marketplace="EBAY_DE",
    #     marketplace_id="EBAY_DE",
    #     deliveryCountry="DE",
    #     item_to_fetch=1,
    #     price_anpassen=1,
    #     sale_price_anpassen=0.8,
    #     is_use_image_service=False,
    #     target_category_name_in_woocommerce="Sonstige"
    # ),
    # FetchConfigModel(
    #     legacy_item_id=377494682430,
    #     legacy_variation_id=645800639898,
    #     marketplace="EBAY_DE",
    #     marketplace_id="EBAY_DE",
    #     deliveryCountry="DE",
    #     item_to_fetch=1,
    #     price_anpassen=1,
    #     sale_price_anpassen=0.8,
    #     is_use_image_service=False,
    #     target_category_name_in_woocommerce="Sonstige"
    # ),
    # FetchConfigModel(
    #     legacy_item_id=377494682430,
    #     legacy_variation_id=645800639899,
    #     marketplace="EBAY_DE",
    #     marketplace_id="EBAY_DE",
    #     deliveryCountry="DE",
    #     item_to_fetch=1,
    #     price_anpassen=1,
    #     sale_price_anpassen=0.8,
    #     is_use_image_service=False,
    #     target_category_name_in_woocommerce="Sonstige"
    # ),
    # FetchConfigModel(
    #     legacy_item_id=377494682430,
    #     legacy_variation_id=645800639900,
    #     marketplace="EBAY_DE",
    #     marketplace_id="EBAY_DE",
    #     deliveryCountry="DE",
    #     item_to_fetch=1,
    #     price_anpassen=1,
    #     sale_price_anpassen=0.8,
    #     is_use_image_service=False,
    #     target_category_name_in_woocommerce="Sonstige"
    # ),
    # FetchConfigModel(
    #     legacy_item_id=377494682430,
    #     legacy_variation_id=645800639901,
    #     marketplace="EBAY_DE",
    #     marketplace_id="EBAY_DE",
    #     deliveryCountry="DE",
    #     item_to_fetch=1,
    #     price_anpassen=1,
    #     sale_price_anpassen=0.8,
    #     is_use_image_service=False,
    #     target_category_name_in_woocommerce="Sonstige"
    # ),
    # FetchConfigModel(
    #     legacy_item_id=377494682430,
    #     legacy_variation_id=645800639902,
    #     marketplace="EBAY_DE",
    #     marketplace_id="EBAY_DE",
    #     deliveryCountry="DE",
    #     item_to_fetch=1,
    #     price_anpassen=1,
    #     sale_price_anpassen=0.8,
    #     is_use_image_service=False,
    #     target_category_name_in_woocommerce="Sonstige"
    # ),
    # FetchConfigModel(
    #     legacy_item_id=377494682430,
    #     legacy_variation_id=645800639903,
    #     marketplace="EBAY_DE",
    #     marketplace_id="EBAY_DE",
    #     deliveryCountry="DE",
    #     item_to_fetch=1,
    #     price_anpassen=1,
    #     sale_price_anpassen=0.8,
    #     is_use_image_service=False,
    #     target_category_name_in_woocommerce="Sonstige"
    # )
]

# --
# ...
# --


def reduce_image_size(image_directory_model:ImageDirectoryModel):
    SetupMarketConnectorController().image_provider.image_processing_pipeline.reduce_image_size(image_directory_model)


def white_backgroung(image_directory_model:ImageDirectoryModel):
    SetupMarketConnectorController().image_provider.image_processing_pipeline.white_backgroung(image_directory_model)


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
        MarketConnectorController.sync_ebay_to_woocommerce(fetch_config_model=search_in_ebay_model)


#  MarketConnectorController.create_ebay_offers(search_in_ebay_model=search_in_ebay_model)


def sync_woocommerce_to_ebay():
    for search_in_woocommerce_model in search_in_woocommerce_models:
        MarketConnectorController.sync_woocommerce_to_ebay(fetch_config_model=search_in_woocommerce_model)


def sync_zalando_lounge_to_woocommerce():
    for search_in_zalando_lounge_model in search_in_zalando_lounge_models:
        MarketConnectorController.sync_zalando_lounge_to_woocommerce(fetch_config_model=search_in_zalando_lounge_model)


def sync_matterhorn_moda_to_woocommerce():
    for fetch_matterhorn_moda_config_model in fetch_matterhorn_moda_config_models:
        MarketConnectorController.sync_matterhorn_moda_to_woocommerce(fetch_config_model=fetch_matterhorn_moda_config_model)


# sync_matterhorn_moda_to_woocommerce()
sync_ebay_to_woocommerce()