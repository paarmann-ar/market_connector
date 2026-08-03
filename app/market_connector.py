from apis.ebay_api.models.search_in_ebay_model import SearchInEbayModel
from app.controller.market_connector_controller import MarketConnectorController

# --
# ...
# --

# target_woocommerce_category_model_name = "PLC & SPS"

# search_in_ebay_model = SearchInEbayModel(
#     category_name_candidate="SPS-Prozessoren",
#     conditions="{NEW,USED}",
#     deliveryCountry="DE",
#     q="Siemens 6ES7215-1HG40-0XB0 6ES7 215-1HG40-0XB0",
# )

target_woocommerce_category_model_name = "Elektronik"

search_in_ebay_model = SearchInEbayModel(
    # category_name_candidate="Business & Industrie",
    conditions="{NEW,USED}",
    deliveryCountry="DE",
    q="RM1-XA",
)


def upload_from_ebay_to_woocommerce():
    market_connector_controller = MarketConnectorController()
    market_connector_controller.fetch_from_ebay(
        search_in_ebay_model=search_in_ebay_model
    )
    market_connector_controller.convert_ebay_to_woocommerce_product_model()
    market_connector_controller.upload_model_to_woocommerce(
        target_woocommerce_category_name=target_woocommerce_category_model_name
    )


upload_from_ebay_to_woocommerce()
