from app.core.base import Base

# --
# ...
# --


class MarketConnectorController(Base):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.woocommerce_product_models = []


    # --
    # ...
    # --

    def fetch_from_ebay(self):
        self.ebay.get_all_product_ids(
            category_name_candidate="Sonstige Sensoren",
            filter_product="conditions:{NEW},deliveryCountry:DE",
            q="Lambdasonde",
        )
        self.ebay.get_all_data_of_product_with_product_id_from_products_list()

    # --
    # ...
    # --

    def convert_ebay_to_woocommerce_product_model(self):


        for product in self.ebay.product_detail_list:
            woocommerce_image_model = self.woocommerce_image_model()

            self.woocommerce_product_models.append(
                self.woocommerce_product_model(
                    product["title"],
                    name=f"{product['title']} - {product['condition']}",
                    slug="",
                    permalink="",
                    catalog_visibility="visible",
                    description=product["description"],
                    short_description=product["shortDescription"],
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
                    categories=[{"id": 1}],
                    brands=[product["brand"]],
                    tags=[f"{product['condition']} - {product['brand']}"],
                    images=[woocommerce_image_model],
                )
            )

        self.prompt_on_screen(self.woocommerce_product_models)

    # --
    # ...
    # --

    def upload_model_to_woocommerce(self):
        for product_model in self.woocommerce_product_models:
            self.woocommerce.woocommerce_product.upload_products(products_model=product_model)