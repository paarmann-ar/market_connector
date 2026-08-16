from apis.ebay_api.models.search_in_ebay_model import SearchInEbayModel
from app.controller.market_connector_controller import MarketConnectorController

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

    market_connector_controller.image_convertor_pipline(woocommerce_product_models = woocommerce_product_models)

    market_connector_controller.upload_model_to_woocommerce(woocommerce_product_models = woocommerce_product_models, search_in_ebay_model=search_in_ebay_model)


# q=[
#     "Q6135-LE",
#     "Q6135-E",
#     "Q6135",
#     "AXIS Q6135",
#     "AXIS Q6135-LE",
#     "AXIS P6135",
# ],
# q = "Q6135-LE 50HZ"

# target_woocommerce_category_model_name = "Sonstige"
# search_in_ebay_model = SearchInEbayModel(
# #     category_name_candidate="Business & Industrie",
#     conditions="{NEW}",
#     deliveryCountry="DE",
#     q="Axis Q6135-LE PTZ",

# )
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW|USED}",
#     # deliveryCountry="DE",
#     q="Axis Q6315-LE PTZ",
# )


# target_woocommerce_category_model_name = "Messtechnik"
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW|USED}",
#     deliveryCountry="DE",
#     q="GE Panametrics C-PT-10-N-B-EX-O",
# )


#################
# target_woocommerce_category_model_name = "Sensoren"
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="SPS-Prozessoren",
#     conditions="{NEW|USED}",
#     deliveryCountry="DE",
#     q="nox lambda sensor siemens ns11a",
# )
#################
# target_woocommerce_category_model_name = "Sensoren"
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW|USED}",
#     deliveryCountry="DE",
#     q="Bühler Niveau Temperatur Schalter Bühler Technologies NV71D-HY-MS-2M12/750-2K-2T-BFA"
# )


# target_woocommerce_category_model_name = "Sensoren"
# # search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW|USED}",
#     deliveryCountry="DE",
#     q="Sick Induktiver Näherungssensor IME18-08NPSZT0S proximity sensor 1068737"
# )
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW|USED}",
#     deliveryCountry="DE",
#     q="BALLUFF BGL001M BGL 50A-003-S49 BGL50A003S49! NEU!",item_to_fetch=2,
# )
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW|USED}",
#     deliveryCountry="DE",
#     q="BALLUFF BGL001M BGL 50A-003-S49 BGL50A003S49! NEU!",
#     item_to_fetch=2,
# )
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW|USED}",
#     deliveryCountry="DE",
#     q="IFM electronic IA5063 IAE3010-APKG Induktiver Sensor unbenutzt ohne OVP"
# )
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW|USED}",
#     deliveryCountry="DE",
#     q="Ifm electronic IA5051 IA-3010-APKG Induktiver Sensor -unused-"
# )
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW}",
#     deliveryCountry="DE",
#     q="BOSCH LAMBDASONDE LAMDASONDE DIAGNOSESONDE NACH KAT 0258006499",
#     item_to_fetch=2,
#     target_category_name_in_woocommerce="Sensoren",
# )
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW|USED}",
#     deliveryCountry="DE",
#     q="Ifm electronic IA5051 IA-3010-APKG Induktiver Sensor -unused-
# )


# target_woocommerce_category_model_name = "Sensoren"
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW|USED}",
#     marketplace="EBAY_DE",
#     deliveryCountry="DE",
#     q="Bühler NT M-MS-G3/4-M3/250-1K Niveau-Temperaturschalter",
#     item_to_fetch=2,

# )

# target_woocommerce_category_model_name = "Sensoren"
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW}",
#     deliveryCountry="DE",
#     marketplace="EBAY_DE",
#     q="NEU Stickoxid Nox Sensor 68366428AA SNS0932 für Jeep Compass II MP M6 1.6 CRD",
#     item_to_fetch=1,
# )

# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW}",
#     deliveryCountry="DE",
#     marketplace="EBAY_DE",
#     q="Buhler NT M-VA-G3/4-M12/170-2K-ATEX Niveau-Und Temperaturkontakt",
#     item_to_fetch=3,
# )


# target_woocommerce_category_model_name = "Sensoren"
# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="SPS-Prozessoren",
#     conditions="{NEW}",
#     deliveryCountry="DE",
#     q="Niveau- und Temperaturschalter",
#     item_to_fetch=10
# )
# product: Temperaturbeständiger Schwimmer-Niveauschalter für saure und alkalische Lösun
# product: Temperaturbeständiger Schwimmer-Niveauschalter für Säure- und Laugenlösungen
# product: febi Sensor Kühlmittelstandssensor für OPEL ASTRA H J ZAFIRA TOURER C CASCADA
# product: Metzger 0901108 Sensor für Kühlmittelstand Sensor für Kühlmittelstand
# product: Sensor, Kühlmittelstand METZGER 0901108 ORIGINAL ERSATZTEIL für OPEL
# product: Bühler NT 66-MS-S6/370/2K-TT71-KT Niveau- und Temperaturschalter Unused
# product: ENGLER Niveau- und Temperaturschalter SSM.4.ABCD5....275.18S1
# search_in_ebay_model = SearchInEbayModel(
#     conditions="{NEW}",
#     marketplace="EBAY_DE",
#     deliveryCountry="DE",
#     q="Bühler NT 66-MS-S6/370/2K-TT71-KT Niveau- und Temperaturschalter Unused",
#     item_to_fetch=2,
#     price_anpassen = 1.5
# )


# target_woocommerce_category_model_name = "PLC & SPS"
# # search_in_ebay_model = SearchInEbayModel(
# #     # category_name_candidate="SPS-Prozessoren",
# #     q="Siemens 6ES7215-1HG40-0XB0 6ES7 215-1HG40-0XB0",
# # )


# search_in_ebay_model = SearchInEbayModel(
#     # category_name_candidate="Business & Industrie",
#     conditions="{NEW}",
#     deliveryCountry="DE",
#     q="Siemens Simatic S7-1500 6ES7512-1CK01-0AB0",
#     item_to_fetch=1,
# )


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
    # SearchInEbayModel(
    #     conditions="{NEW}",
    #     marketplace="EBAY_US",
    #     deliveryCountry="US",
    #     q="FITOK",
    #     filter="sellers:{jlb_the_farm},price:[..500]",
    #     item_to_fetch=1,
    #     price_anpassen=1.5,
    # )
# ABB SSAC PLMU11 PC606 3-Phasen Spannungsüberwachungsrelais 200-480VAC SPDT 8-Pin
# DAIHATSU PUG-AP65W ELEKTRISCHER MAGNETISCHER AUFNEHMER SENSOR 15190A-
# Speed Controller/Motor Display Rate Variable/AC 220V Motor Governor.
# AC 110-230V 10000W SCR Motor Speed Controller Volt Regulator Dimmer Thermostat
# 2-Phasen 4,2A Schrittmotortreiber-
# PWM 12V 24V 36V 48V DC Motor Speed Controller Reversible Switch 6A Regulator
search_in_ebay_models = [
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
        SearchInEbayModel(
        conditions="{NEW}",
        marketplace="EBAY_DE",
        deliveryCountry="DE",
        q="",
        legacy_item_id="398250185440",
        item_to_fetch=1,
        price_anpassen=1.8,
        target_category_name_in_woocommerce="Tischdekoration"
    ),
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


def start():
    for search_in_ebay_model in search_in_ebay_models:
        print(search_in_ebay_model.q)
        upload_from_ebay_to_woocommerce_pipline(search_in_ebay_model=search_in_ebay_model)


start()


        # // "base_url": "https://www.paarmann-tech.de/wp-json/wc/v3"
        # // "consumer_key": "ck_db0adcfd3b7c3b3fb117d245a0ea648951869584"
        # // "consumer_secret": "cs_1767d6b43ab0bda2c4f71aaa0768ff36c42369a7"