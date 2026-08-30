from apis.ebay_api.models.browse.product_ebay_model import ProductEbayModel
from apis.woocommerce_api.models.woocommerce_tag_model import WoocommerceTagModel
from market_services.meta_data_services.meta_data_services import MetaDataServices
from apis.woocommerce_api.models.woocommerce_brand_model import WoocommerceBrandModel
from apis.woocommerce_api.models.woocommerce_category_model import WoocommerceCategoryModel
from toolboxs.random_expertion import RandomExpertion

from apis.woocommerce_api.models.woocommerce_product_model import WoocommerceProductModel
from toolboxs.numbers import Numbers
from apis.woocommerce_api.models.woocommerce_image_model import WoocommerceImageModel
from market_services.adapters.ebay.ebay_product_model_to_product_input_metadata_model import EbayProductModelToProductInputMetadataModel
from market_services.adapters.models.validate_final_model import ValidateFinalModel

# --
# ...
# --


class EbayProductModelToWoocommerceProductModelAdaptor:
    def adapter(self, product_ebay_model: ProductEbayModel) -> WoocommerceProductModel:

        # badan por konam ta roll har befrestam vase validation, alan to hadcode hastan
        validate_final_model = ValidateFinalModel(validation_roles=[])
        validate_final_model = None

        meta_data_services = MetaDataServices()
        product_output_metadata_model = meta_data_services.create_metadata(
            product_input_metadata_model=EbayProductModelToProductInputMetadataModel().adapter(
                product_ebay_model=product_ebay_model, prompt_filename="paarmann-tech_product_ebay_model"
            ),
            validate_final_model=validate_final_model,
        )

        woocommerce_tags_model = []
        for tag in product_output_metadata_model.product_tags:
            woocommerce_tag_model = WoocommerceTagModel(name=tag)
            woocommerce_tags_model.append(woocommerce_tag_model)

        woocommerce_images_model: list = []
        image_alt = product_output_metadata_model.image_seo_model.get("image_alt")
        image_alt_main = product_output_metadata_model.image_seo_model.get("image_alt_main")

        woocommerce_images_model.insert(
            0, WoocommerceImageModel().from_api({"src": product_ebay_model.image.imageUrl, "alt": image_alt_main})
        )

        for image_url in product_ebay_model.additionalImages:
            woocommerce_images_model.append(WoocommerceImageModel.from_api({"src": image_url.imageUrl, "alt": image_alt}))

        return WoocommerceProductModel(
            categories=WoocommerceCategoryModel(name=product_ebay_model.categoryPath.split("|")[-1]),
            brands=[WoocommerceBrandModel(name=product_ebay_model.brand)],
            tags=woocommerce_tags_model,
            slug=product_output_metadata_model.slug,
            meta_data=product_output_metadata_model.seo_model,
            name=product_output_metadata_model.title,
            description=product_output_metadata_model.description,
            short_description=product_output_metadata_model.short_description,
            price=Numbers.price_anpassen(product_ebay_model.price["value"], product_ebay_model.price_anpassen),
            regular_price=Numbers.price_anpassen(product_ebay_model.price["value"], product_ebay_model.price_anpassen),
            sale_price=Numbers.price_anpassen(product_ebay_model.price["value"], (product_ebay_model.price_anpassen - 0.1)),
            images=woocommerce_images_model,
            image_description=product_output_metadata_model.image_description,
            sku=RandomExpertion.sku_generator(),
        )
