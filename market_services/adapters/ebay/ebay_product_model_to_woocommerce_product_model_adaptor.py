from apis.ebay_api.models.browse.product_ebay_model import ProductEbayModel
from apis.woocommerce_api.models.woocommerce_brand_model import WoocommerceBrandModel
from apis.woocommerce_api.models.woocommerce_category_model import WoocommerceCategoryModel
from apis.woocommerce_api.models.woocommerce_image_model import WoocommerceImageModel
from apis.woocommerce_api.models.woocommerce_product_model import WoocommerceProductModel
from apis.woocommerce_api.models.woocommerce_tag_model import WoocommerceTagModel
from market_services.adapters.ebay.ebay_product_model_to_product_input_metadata_model import EbayProductModelToProductInputMetadataModel
from market_services.adapters.ebay.ebay_assemble_final import assemble_final
from market_services.meta_data_services.meta_data_services import MetaDataServices
from toolboxs.numbers import Numbers
from toolboxs.random_expertion import RandomExpertion
from typing import Optional

# --
# ...
# --


class EbayProductModelToWoocommerceProductModelAdaptor:
    def adapter(self, product_ebay_model: ProductEbayModel) -> WoocommerceProductModel:

        meta_data_services = MetaDataServices()
        product_output_metadata_model = meta_data_services.create_metadata(
            product_input_metadata_model=EbayProductModelToProductInputMetadataModel().adapter(
                product_ebay_model=product_ebay_model, prompt_filename="paarmann-tech_product_ebay_model"
            ),
            assemble_final=assemble_final,
            product_model=product_ebay_model,
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

        if product_ebay_model.additionalImages:
            for image_url in product_ebay_model.additionalImages:
                woocommerce_images_model.append(WoocommerceImageModel.from_api({"src": image_url.imageUrl, "alt": image_alt}))

        return WoocommerceProductModel(
            categories=self._get_categories(product_ebay_model=product_ebay_model),
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
            on_sale=True,
            manage_stock=True,
            stock_quantity=product_ebay_model.estimatedAvailabilities[0]['estimatedRemainingQuantity'],
            stock_status=self._get_stock_status(product_ebay_model)
        )

# --
# ...
# --

    def _get_categories(
        self,
        product_ebay_model: ProductEbayModel,
    ) -> list[WoocommerceCategoryModel]:

        category_name = product_ebay_model.categoryPath.split("|")[-1]
        category_path = product_ebay_model.categoryPath

        return [WoocommerceCategoryModel(name=category_name, slug=self._slugify(category_name), path=category_path)]

# --
# ...
# --

    @staticmethod
    def _slugify(value: Optional[str]) -> Optional[str]:

        if not value:
            return None

        return value.strip().lower().replace(" ", "-")
# --
# ...
# --

    def _get_stock_status(
        self,
        product_ebay_model: ProductEbayModel,
    ) -> str:

        if (product_ebay_model.estimatedAvailabilities[0]['estimatedRemainingQuantity'] or 0) > 0:
            return "instock"

        return "outofstock"