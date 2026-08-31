import CONSTS
from apis.woocommerce_api.core.base_woocommerce_api import BaseWoocommerceApi
from apis.wordpress_api.wordpress_api import WordpressApi

# --
# ...
# --


# hanooz takmilesh nakardam
class ImageProduceController(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.image_folder_adress = f"{CONSTS.IMAGE_FILES}/temp/"
        self.wordpress_api = WordpressApi()

    #  --
    #  ...
    #  --

    def download_image_form_url_save_in_disk(self, src: str, image_name: str) -> str:

        try:
            response = self.request(
                method="get",
                url=src,
                is_download_file=True,
            )

            with open(f"{CONSTS.IMAGE_FILES}/temp/{image_name}", "wb") as image_file:
                image_file.write(response.content)

            self.prompt_on_screen(f"get product modele: {response}")

            return response

        except Exception as exp:
            self.prompt_on_screen(f"get_product_by_name: {exp}")

    #  --
    #  ...
    #  --

    def upload_image_from_disk_to_wordpress(self, file_address: str) -> int:

        self.wordpress_api.wordpress_media_model.media_address = CONSTS.IMAGE_FILES / temp

        self.wordpress_api.upload_media_models_from_disk()
