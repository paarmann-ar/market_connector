from apis.ebay_api.models.search_in_ebay_model import SearchInEbayModel
from app.core.base import Base
from bs4 import BeautifulSoup
from apis.woocommerce_api.models.woocommerce_category_model import WoocommerceCategoryModel
from apis.apis_provider import ApisProvider

# --
# ...
# --


class MarketConnectorController(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.apis_provider = ApisProvider()
        self.woocommerce_product_models = []

    # --
    # ...
    # --

    def fetch_from_ebay(self, search_in_ebay_model: SearchInEbayModel):
        search_in_ebay_model = search_in_ebay_model.to_dict()

        self.apis_provider.ebay_api.get_all_product_ids(
            category_name_candidate=search_in_ebay_model.get("category_name_candidate"),
            filter_product=search_in_ebay_model.get("filter_product"),
            q=search_in_ebay_model.get("q"),
        )

        self.apis_provider.ebay_api.get_all_data_of_product_with_product_id_from_products_list()

    # --
    # ...
    # --

    def convert_ebay_to_woocommerce_product_model(self) -> None:

        for product in self.apis_provider.ebay_api.product_detail_list:
            woocommerce_categories_model: list = []
            woocommerce_brands_model: list = []
            woocommerce_tags_model: list = []
            woocommerce_images_model: list = []

            woocommerce_images_model.insert(
                0,
                self.apis_provider.woocommerce_api.woocommerce_image_model.from_api(
                    {"src": product.get("image")["imageUrl"]}
                ),
            )
            for image_url in product.get("additionalImages", []):
                woocommerce_images_model.append(
                    self.apis_provider.woocommerce_api.woocommerce_image_model.from_api(
                        {"src": image_url["imageUrl"]}
                    )
                )

            # chon faghat akharin category mikhastam dashteh basham
            category = product["categoryPath"].split("|")[-1]
            woocommerce_categories_model.append(
                self.apis_provider.woocommerce_api.woocommerce_category_model(name=category)
            )

            woocommerce_brands_model.append(
                self.apis_provider.woocommerce_api.woocommerce_brand_model(name=product["brand"])
            )

            woocommerce_tag_parser_model = self.apis_provider.woocommerce_api.woocommerce_tag_parser().woocommerce_tag_parser(
                context=f"{product['title']} {product.get('brand')} {product.get('condition')} {product.get('sku')}"
            )

            for tag in woocommerce_tag_parser_model.tags:
                woocommerce_tag_model = self.apis_provider.woocommerce_api.woocommerce_tag_model()
                woocommerce_tag_model.name = tag
                woocommerce_tags_model.append(woocommerce_tag_model)

            self.woocommerce_product_models.append(
                self.apis_provider.woocommerce_api.woocommerce_product_model(
                    name=f"{product['title']} - {product['condition']}",
                    slug="",
                    permalink="",
                    catalog_visibility="visible",
                    description=BeautifulSoup(
                        product.get("description", ""), "html.parser"
                    ).get_text(separator=" ", strip=True),
                    short_description=BeautifulSoup(
                        product.get("shortDescription", ""), "html.parser"
                    ).get_text(separator=" ", strip=True),
                    sku="",
                    price=str(round(float(product["price"]["value"]) * 1.3)),
                    regular_price=str(round(float(product["price"]["value"]) * 1.3)),
                    sale_price=str(round(float(product["price"]["value"]) * 1.3)),
                    on_sale=True,
                    tax_status="taxable",
                    tax_class="",
                    manage_stock=False,
                    shipping_required=True,
                    shipping_taxable=True,
                    shipping_class="",
                    shipping_class_id=0,
                    stock_status="instock",
                    categories=woocommerce_categories_model,
                    brands=woocommerce_brands_model,
                    tags=woocommerce_tags_model,
                    images=woocommerce_images_model,
                )
            )

        self.prompt_on_screen(self.woocommerce_product_models)

    # --
    # ...
    # --

    def upload_model_to_woocommerce(self, target_woocommerce_category_model:WoocommerceCategoryModel) -> bool:
        for product_model in self.woocommerce_product_models:
            product_model.categories = [target_woocommerce_category_model]
             self.apis_provider.woocommerce_api.woocommerce_uploader.resolve_or_upload(product_model=product_model)

            self.delay(500)

        self.apis_provider.woocommerce_api.woocommerce_rollback.rollback()
        return True
