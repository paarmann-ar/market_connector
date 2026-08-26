from apis.woocommerce_api.config.woocommerce_api_config import (
    WoocommerceApiConfig,
)
from apis.woocommerce_api.core.base_woocommerce_api import (
    BaseWoocommerceApi,
)
from apis.woocommerce_api.models.woocommerce_review_model import WoocommerceReviewModel

# --
# ...
# --


class WoocommerceReview(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.base_url = self.config_dictionary.get("base_url")
        self.wp_media_url = self.config_dictionary.get("wp_media_url")

        self.consumer_key = self.config_dictionary.get("consumer_key")
        self.consumer_secret = self.config_dictionary.get("consumer_secret")

        self.wp_user = self.config_dictionary.get("wp_user")
        self.wp_password = self.config_dictionary.get("wp_password")

        self.review_url = self.config_dictionary.get("review_url")

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return WoocommerceApiConfig().get_dictionary()

    # --
    # ...
    # --

    def __call__(self, category_id) -> str:
        self.get_all_reviews()

    # --
    # ...
    # --

    def get_all_reviews(self, product_id: str, record_per_page: int = 100):
        try:
            response = self.request(
                method="get",
                url=f"{self.base_url}{self.review_url}",
                auth=(self.consumer_key, self.consumer_secret),
                params={"per_page": record_per_page, "product": product_id},
            )

            woocommerce_review_models = []
            for review in response:
                woocommerce_review_models.append(WoocommerceReviewModel.from_api(review))

            return woocommerce_review_models

        except Exception as exp:
            self.prompt_on_screen(f"get_all_reviews: {exp}")

    # --
    # ...
    # --

    def upload_review(self, review_model: WoocommerceReviewModel):

        try:
            response = self.request(
                method="post",
                url=f"{self.base_url}{self.review_url}",
                auth=(self.consumer_key, self.consumer_secret),
                json=review_model.to_dict(),
            )

            self.prompt_on_screen(f"brands: {response}")

            woocommerce_brand_model = WoocommerceReviewModel.from_api(response)
            return woocommerce_brand_model

        except Exception as exp:
            self.prompt_on_screen(f"upload_review: {exp}")
