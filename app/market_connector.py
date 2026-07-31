from app.core.base import Base
from app.controller.market_connector_controller import MarketConnectorController

# --
# ...
# --

market_connector_controller = MarketConnectorController()
market_connector_controller.fetch_from_ebay()
market_connector_controller.convert_ebay_to_woocommerce_product_model()