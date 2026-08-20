from apis.ebay_api.models.browse.product_ebay_model import ProductEbayModel
from market_services.meta_data_services.models.product_input_metadata_model import ProductInputMetadataModel
from market_services.core.clean_product_description import CleanProductDescription
from toolboxs.numbers import Numbers
from toolboxs.text import Text
from toolboxs.html import Html

# --
# ...
# --


class EbayProductModelToProductInputMetadataModel:
    def adapter(self, product_ebay_model: ProductEbayModel) -> ProductInputMetadataModel:
        return ProductInputMetadataModel(
            cache_id=product_ebay_model.itemId,
            title=product_ebay_model.title,
            description=Html.remove_html_tags(
                context=CleanProductDescription.clean_product_description(text=product_ebay_model.description)
            )[:1500],
            short_description=Html.remove_html_tags(context=product_ebay_model.shortDescription)[:500],
            brand=product_ebay_model.brand,
            condition=product_ebay_model.condition,
            mpn=product_ebay_model.mpn,
        )
