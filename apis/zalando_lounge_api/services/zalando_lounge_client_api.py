from playwright.sync_api import sync_playwright

from apis.core.base import Base
from apis.zalando_lounge_api.config.zalando_lounge_api_config import ZalandoLoungeApiConfig
from apis.zalando_lounge_api.models.zalando_lounge_product_model import ZalandoLoungeProductModel

# --
# ...
# --


class ZalandoLoungeClientApi(Base):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.base_url = self.config_dictionary.get("base_url")
        self.catalog_url = self.config_dictionary.get("catalog_url")
        self.campaigns = self.config_dictionary.get("campaigns")
        self.articles = self.config_dictionary.get("articles")

    #  --
    #  ...
    #  --

    @classmethod
    def get_config_dictionary(cls):
        return ZalandoLoungeApiConfig().get_dictionary()

    #  --
    #  ...
    #  --

    def connect(self):

        self.playwright = sync_playwright().start()

        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir="./zalando_browser",
            headless=False,
            locale="de-DE",
        )

        self.page = self.context.new_page()
        self.page.goto(f"{self.base_url}")
        self.page.locator(selector="//span[text()='Einloggen']").click()

        self.page.get_by_test_id("verify-email-input").fill("paarmann-ara@hotmail.com")
        self.page.get_by_test_id("verify-email-button").click()

        self.page.locator("#password").fill("@25340Pedram")
        self.page.locator('[data-testid="login-button"]').click()

        self.cookies = {
            cookie["name"]: cookie["value"]
            for cookie in self.context.cookies()
            if cookie.get("domain", "").lstrip(".").endswith("zalando-lounge.de")
        }

    #  --
    #  ...
    #  --

    def get_zalando_lounge_products_by_campaign_artikel_sku(self, campaign_id: str, sku: str) -> ZalandoLoungeProductModel:

        try:
            response = self.request(
                is_use_default_headers=False,
                method="get",
                url=f"{self.base_url}/api/phoenix/catalog/events/{campaign_id}/articles/{sku}/similar",
                headers={
                    "accept": "application/json, text/plain, */*",
                    "accept-language": "en-US,en;q=0.9,de;q=0.8",
                    "client_type": "web",
                    "referer": f"{self.base_url}/campaigns/{campaign_id}/articles/{sku}?navigationSource=catalog&catalog-type=campaign",
                    "sec-ch-ua": ('"Not=A?Brand";v="99", "Google Chrome";v="151", "Chromium";v="151"'),
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"macOS"',
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-origin",
                    "user-agent": (
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/151.0.0.0 Safari/537.36"
                    ),
                    "x-requested-with": "XMLHttpRequest",
                },
                cookies=self.cookies,
            )

            print(response)

        except Exception as exp:
            self.prompt_on_screen(f"get_zalando_lounge_products_by_campaign_artikel_sku: {exp}")
