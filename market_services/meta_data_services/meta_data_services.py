from apis.seo_api.models.rank_math_model import RankMathModel
from ki.ki_provider import KiProvider
from ki.models.input_message_model import InputMessageModel
from market_services.meta_data_services.models.product_input_metadata_model import ProductInputMetadataModel
from market_services.meta_data_services.models.product_output_metadata_model import ProductOutputMetadataModel
from toolboxs.text import Text
from apis.matterhorn_moda_api.models.product_matterhorn_moda_model import ProductMatterhornModaModel
from ki.ollama.models.ollama_answer_model import ProductOutputModel


# --
# ...
# --
class MetaDataServices:
    def __init__(self):
        self.ollama = KiProvider().ollama

    # --
    # ...
    # --

    def create_metadata(self, product_input_metadata_model: ProductInputMetadataModel, assemble_final, product_model:object) -> ProductOutputMetadataModel:

        inputs = product_input_metadata_model.to_dict()
        input_message_model = InputMessageModel(inputs=inputs)
        input_message_model.md_file_name = inputs.get("prompt_filename")
        # qwen3:30B

        if input_message_model.md_file_name:
            product_output_model = self.ollama.get_seo_from_ollama_generate_for_rankmath(input_message_model=input_message_model)

        else:
            product_output_model = ProductOutputModel(inputs)
        # -----------------------------------------
        # Normalize KI response
        # -----------------------------------------

        product_output_metadata_model = assemble_final(
            product_output_model=product_output_model, product_input=product_input_metadata_model, product_model=product_model
        )

        # -----------------------------------------
        # Image SEO
        # -----------------------------------------

        image_alt_constructor = " ".join(keyword for keyword in product_output_metadata_model.focus_keywords if keyword)
        image_alt = Text().remove_duplicate_words_from_string(image_alt_constructor)
        image_alt_main = product_output_metadata_model.title.split("|")[0].strip()

        # -----------------------------------------
        # Output model
        # -----------------------------------------

        product_output_metadata_model.image_seo_model = {
            "image_alt": image_alt,
            "image_alt_main": image_alt_main,
        }

        rank_math_focus_keyword = f"{product_input_metadata_model.mpn}, {product_input_metadata_model.brand}{', '.join(product_output_metadata_model.focus_keywords)}, {product_output_metadata_model.primary_focus_keyword}"

        product_output_metadata_model.seo_model = RankMathModel(
            rank_math_title=product_output_metadata_model.title,
            rank_math_description=product_output_metadata_model.description,
            rank_math_focus_keyword=rank_math_focus_keyword,
        ).for_use_in_woocommerce()

        return product_output_metadata_model
