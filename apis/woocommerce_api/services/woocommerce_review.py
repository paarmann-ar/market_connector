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

    # --
    # ...
    # --

    def resolve_or_upload(self, woocommerce_review_model: WoocommerceReviewModel):

        review = self.get_brand_by_name(woocommerce_review_model.name)

        if review:
            return review

        return self.upload_review(WoocommerceReviewModel(name=woocommerce_review_model.name))


# --
# ...
# --

# def delete_brand_by_brand_id(self, brand_id: int):

#     try:
#         response = self.request(
#             method="delete",
#             url=f"{self.base_url}{self.brand_url}/{brand_id}",
#             auth=(self.consumer_key, self.consumer_secret),
#             params={"force": True},
#         )

#         self.prompt_on_screen(f"brand deleted: {response}")

#         return response

#     except Exception as exp:
#         self.prompt_on_screen(f"delete_brand_by_brand_id: {exp}")
