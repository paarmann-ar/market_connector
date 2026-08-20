from apis.seo_api.models.rank_math_model import RankMathModel
from ki.ki_provider import KiProvider
from ki.prompt_provider.models.input_message_model import InputMessageModel
from market_services.meta_data_services.models.product_input_metadata_model import ProductInputMetadataModel
from market_services.meta_data_services.models.product_output_metadata_model import ProductOutputMetadataModel
from toolboxs.text import Text


# --
# ...
# --
class MetaDataServices:
    def __init__(self):
        self.ollama = KiProvider().ollama

    # --
    # ...
    # --

    def create_metadata(
        self,
        product_input_metadata_model: ProductInputMetadataModel,
    ) -> ProductOutputMetadataModel:

        inputs = product_input_metadata_model.to_dict()
        input_message_model = InputMessageModel(inputs=inputs)
        input_message_model.md_file_name = "product_content"
        ki_message = self.ollama.get_seo_from_ollama_generate_for_rankmath(input_message_model=input_message_model)

        # -----------------------------------------
        # Normalize KI response
        # -----------------------------------------

        title = ki_message.get("title") or ""
        description = ki_message.get("description") or ""
        focus_keyword = ki_message.get("focus_keyword") or ""
        focus_keywords = ki_message.get("focus_keywords") or []

        if isinstance(focus_keywords, str):
            focus_keywords = [focus_keywords]

        # -----------------------------------------
        # Image SEO
        # -----------------------------------------

        alt_image_constructor = " ".join(keyword for keyword in focus_keywords if keyword)
        image_alt = Text().remove_duplicate_words_from_string(alt_image_constructor)
        image_alt_main = title.split("|")[0].strip()

        # -----------------------------------------
        # Output model
        # -----------------------------------------

        product_output_metadata_model = ProductOutputMetadataModel(**ki_message)

        product_output_metadata_model.image_seo_model = {
            "image_alt": image_alt,
            "image_alt_main": image_alt_main,
        }

        product_output_metadata_model.seo_model = RankMathModel(
            rank_math_title=title,
            rank_math_description=description,
            rank_math_focus_keyword=focus_keyword,
        ).for_use_in_woocommerce()

        return product_output_metadata_model
