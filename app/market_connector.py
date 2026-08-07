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

# target_woocommerce_category_model_name = "Sonstige"
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW|USED}",
#     deliveryCountry="DE",
#     q="AXIS Q6135",
# )


# target_woocommerce_category_model_name = "PLC & SPS"
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="SPS-Prozessoren",
#     conditions="{NEW|USED}",
#     deliveryCountry="DE",
#     q="Siemens 6ES7215-1HG40-0XB0 6ES7 215-1HG40-0XB0",
# )


# target_woocommerce_category_model_name = "Sensoren"
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="SPS-Prozessoren",
#     conditions="{NEW|USED}",
#     deliveryCountry="DE",
#     q="nox lambda sensor siemens ns11a",
# )

# target_woocommerce_category_model_name = "Sensoren"
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="SPS-Prozessoren",
#     conditions="{NEW|USED}",
#     deliveryCountry="DE",
#     q="anti",
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


target_woocommerce_category_model_name = "Sensoren"
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW|USED}",
#     deliveryCountry="DE",
#     q="Bühler Niveau Temperatur Schalter Bühler Technologies NV71D-HY-MS-2M12/750-2K-2T-BFA",
# )
search_in_ebay_model = SearchInEbayModel(
    # category_name_candidate="Business & Industrie",
    conditions="{NEW|USED}",
    deliveryCountry="DE",
    q="NEU Stickoxid Nox Sensor 68366428AA SNS0932 für Jeep Compass II MP M6 1.6 CRD",
)

# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW|USED}",
#     deliveryCountry="DE",
#     q="Bühler NT M-MS-G3/4-M3/250-1K Niveau-Temperaturschalter",
# )
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW|USED}",
#     deliveryCountry="DE",
#     q="Buhler NT M-VA-G3/4-M12/170-2K-ATEX Niveau-Und Temperaturkontakt",
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
    market_connector_controller.fetch_from_ebay(search_in_ebay_model=search_in_ebay_model)
    market_connector_controller.convert_ebay_to_woocommerce_product_model(price_anpassen=price_anpassen)
    market_connector_controller.upload_model_to_woocommerce(target_woocommerce_category_name=target_woocommerce_category_model_name)


upload_from_ebay_to_woocommerce()
