from apis.ebay_api.models.search_in_ebay_model import SearchInEbayModel
from app.controller.market_connector_controller import MarketConnectorController
from app.controller.setup_market_connector_controller import SetupMarketConnectorController


# --
# ...
# --

def upload_from_ebay_to_woocommerce_pipline(search_in_ebay_model: SearchInEbayModel):
    market_connector_controller = MarketConnectorController()

    product_ebay_models = market_connector_controller.fetch_from_ebay(search_in_ebay_model=search_in_ebay_model)

    for product_ebay_model in product_ebay_models:
        product_ebay_model.price_anpassen = search_in_ebay_model.price_anpassen

    woocommerce_product_models = market_connector_controller.convert_ebay_to_woocommerce_product_model(
        product_ebay_models=product_ebay_models
    )

    market_connector_controller.image_convertor_pipline(woocommerce_product_models=woocommerce_product_models)

    market_connector_controller.upload_model_to_woocommerce(
        woocommerce_product_models=woocommerce_product_models, search_in_ebay_model=search_in_ebay_model
    )



def download_from_ebay_and_create_offer_on_ebay_pipline(search_in_ebay_model: SearchInEbayModel):
    market_connector_controller = MarketConnectorController()

    product_ebay_models = market_connector_controller.fetch_from_ebay(search_in_ebay_model=search_in_ebay_model)

    for product_ebay_model in product_ebay_models:
        product_ebay_model.price_anpassen = search_in_ebay_model.price_anpassen

        product_ebay_model.sku = "sku_test7"

        market_connector_controller.apis_provider.ebay_api.pipeline_create_ebay_offer(
            product_ebay_model=product_ebay_model, marketplace_id="EBAY_DE"
        )

    return


# q=[
#     "Q6135-LE",
#     "Q6135-E",
#     "Q6135",
#     "AXIS Q6135",
#     "AXIS Q6135-LE",
#     "AXIS P6135",
# ],
# q = "Q6135-LE 50HZ"

# product: RM1XA1011 - TÉLÉMÉCANIQUE RM1XA1011 Zubehör Neu
# product: RM1XA1011 - TELEMECHANIK - RM1XA1011 / ZUBEHÖR NEU
# product: TELEMECANIQUE RM1-XA315 MAGNETO-THERMISCHES RELAIS 250-800A
# product: TELEMECANIQUE RM1-XA315 MAGNETO-THERMISCHES RELAIS 250-800A
# product: RM1XA160 020302 SCHNEIDER ELECTRIC, 0, RM1XA160 020302, RM1XA160020302, 0 0 F...
# product: SCHNEIDER ELECTRIC RM1XA016 (020278), Single Pole over Curr Relay16A, 12,5…40...
# product: RM1XA100 020294 SCHNEIDER ELECTRIC, Schneider Electric Einpoliges ..............
# target_woocommerce_category_model_name = "Elektronik"
# search_in_ebay_model = SearchInEbayModel(
#     category_name_candidate="Business & Industrie",
#     conditions="{NEW}",
#     deliveryCountry="DE",
#     q="RM1-XA",
#     item_to_fetch=10,
# )

# target_woocommerce_category_model_name = "Sonstige"
# search_in_ebay_model = SearchInEbayModel(
#     conditions="{NEW}",
#     marketplace="EBAY_US",
#     deliveryCountry="US",
#     q="FITOK",
#     filter="sellers:{jlb_the_farm},price:[..500]",
#     item_to_fetch=1,
#     price_anpassen = 1.5
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
    # SearchInEbayModel(
    #     conditions="{NEW}",
    #     marketplace="EBAY_US",
    #     deliveryCountry="US",
    #     q="ABB SSAC PLMU11 PC606",
    #     item_to_fetch=1,
    #     price_anpassen=1.8,
    #     target_category_name_in_woocommerce="Sensoren"
    # ),
    #     SearchInEbayModel(
    #     conditions="{NEW}",
    #     marketplace="EBAY_US",
    #     deliveryCountry="US",
    #     q="DAIHATSU PUG-AP65W",
    #     item_to_fetch=1,
    #     price_anpassen=1.8,
    #     target_category_name_in_woocommerce="Sensoren"
    # ),
    #     SearchInEbayModel(
    #     conditions="{NEW}",
    #     marketplace="EBAY_US",
    #     deliveryCountry="US",
    #     q="",
    #     legacy_item_id="155291562575",
    #     item_to_fetch=1,
    #     price_anpassen=1.8,
    #     filter="sellers:{life-changing666}",
    #     target_category_name_in_woocommerce="Sensoren"
    # ),
    #     SearchInEbayModel(
    #     conditions="{NEW}",
    #     marketplace="EBAY_US",
    #     deliveryCountry="US",
    #     q="",
    #     legacy_item_id="116715910077",
    #     item_to_fetch=1,
    #     price_anpassen=1.8,
    #     target_category_name_in_woocommerce="Sensoren"
    # ),
    # SearchInEbayModel(
    #         conditions="{NEW}",
    #         marketplace="EBAY_US",
    #         deliveryCountry="US",
    #         q="Siemens Simatic S7-1500 6ES7512-1CK01-0AB0",
    #         legacy_item_id="",
    #         item_to_fetch=1,
    #         price_anpassen=1.8,
    #         target_category_name_in_woocommerce="PLC & SPS"
    #     ),
    # SearchInEbayModel(
    #     conditions="{NEW}",
    #     marketplace="EBAY_DE",
    #     deliveryCountry="DE",
    #     q="",
    #     legacy_item_id="398250185440",
    #     item_to_fetch=1,
    #     price_anpassen=1.8,
    #     target_category_name_in_woocommerce="Tischdekoration",
    # ),
    #     SearchInEbayModel(
    #     conditions="{NEW}",
    #     marketplace="EBAY_US",
    #     deliveryCountry="US",
    #     q="",
    #     legacy_item_id="301905615798",
    #     item_to_fetch=1,
    #     price_anpassen=1.8,
    #     target_category_name_in_woocommerce="Sensoren"
    # ),
    #     SearchInEbayModel(
    #     conditions="{NEW}",
    #     marketplace="EBAY_US",
    #     deliveryCountry="US",
    #     q="",
    #     legacy_item_id="385440556015",
    #     item_to_fetch=1,
    #     price_anpassen=1.8,
    #     target_category_name_in_woocommerce="Sensoren"
    # )
]


def reduce_image_size():
    from image_services.models.image_directory_model import ImageDirectoryModel
    SetupMarketConnectorController().image_provider.image_processing_pipline.reduce_image_size(ImageDirectoryModel())


def setup():
    SetupMarketConnectorController().register_user_token()


def start():
    for search_in_ebay_model in search_in_ebay_models:
        print(search_in_ebay_model.q)
        # upload_from_ebay_to_woocommerce_pipline(search_in_ebay_model=search_in_ebay_model)
        download_from_ebay_and_create_offer_on_ebay_pipline(search_in_ebay_model=search_in_ebay_model)




MarketConnectorController().apis_provider.ebay_api.ebay_inventory.hi()