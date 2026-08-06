from apis.ebay_api.models.search_in_ebay_model import SearchInEbayModel
from app.controller.market_connector_controller import MarketConnectorController

# --
# ...
# --
# q=[
#     "Q6135-LE",
#     "Q6135-E",
#     "Q6135",
#     "AXIS Q6135",
#     "AXIS Q6135-LE",
#     "AXIS P6135",
# ],
# q = "Q6135-LE 50HZ"

price_anpassen = 1.60

# target_woocommerce_category_model_name = "PLC & SPS"
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="SPS-Prozessoren",
#     conditions="{NEW|USED}",
#     deliveryCountry="DE",
#     q="Siemens 6ES7215-1HG40-0XB0 6ES7 215-1HG40-0XB0",
# )

# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW|USED}",
#     deliveryCountry="DE",
#     q="Siemens Simatic S7-1500 6ES7512-1CK01-0AB0",
# )


# target_woocommerce_category_model_name = "Messtechnik"
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW|USED}",
#     deliveryCountry="DE",
#     q="GE Panametrics C-PT-10-N-B-EX-O",
# )

target_woocommerce_category_model_name = "Sonstige"
search_in_ebay_model = SearchInEbayModel(
    # category_name_candidate="Business & Industrie",
    conditions="{NEW|USED}",
    deliveryCountry="DE",
    q="AXIS Q6135",
)


# target_woocommerce_category_model_name = "Sensoren"
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW|USED}",
#     deliveryCountry="DE",
#     q="Bühler Niveau",
# )


# target_woocommerce_category_model_name = "Elektronik"
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW|USED}",
#     deliveryCountry="DE",
#     q="RM1-XA",
# )


def upload_from_ebay_to_woocommerce():
    market_connector_controller = MarketConnectorController()
    market_connector_controller.fetch_from_ebay(
        search_in_ebay_model=search_in_ebay_model
    )
    market_connector_controller.convert_ebay_to_woocommerce_product_model(
        price_anpassen=price_anpassen
    )
    market_connector_controller.upload_model_to_woocommerce(
        target_woocommerce_category_name=target_woocommerce_category_model_name
    )


upload_from_ebay_to_woocommerce()
