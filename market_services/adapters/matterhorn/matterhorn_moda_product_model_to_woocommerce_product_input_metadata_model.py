from apis.matterhorn_moda_api.models.product_matterhorn_moda_model import ProductMatterhornModaModel
from market_services.meta_data_services.models.product_input_metadata_model import ProductInputMetadataModel
from market_services.core.clean_product_description import CleanProductDescription
from toolboxs.numbers import Numbers
from toolboxs.text import Text
from toolboxs.html import Html

# --
# ...
# --


class MatterhornModaProductModelToWoocommerceProductInputMetadataModel:
    def adapter(
        self, product_matterhorn_moda_model: ProductMatterhornModaModel, prompt_filename, is_remove_html=True
    ) -> ProductInputMetadataModel:
        if is_remove_html:
            description = Html.remove_html_tags(
                context=CleanProductDescription.clean_product_description(text=product_matterhorn_moda_model.description)
            )[:1500]
        else:
            description = product_matterhorn_moda_model.description

        return ProductInputMetadataModel(
            cache_id=product_matterhorn_moda_model.id,
            title=product_matterhorn_moda_model.name_without_number,
            description=description,
            brand=product_matterhorn_moda_model.brand,
            prompt_filename=prompt_filename,
        )
