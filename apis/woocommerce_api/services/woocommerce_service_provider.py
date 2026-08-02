class WoocommerceServiceProvider:
    @property
    def woocommerce_product_model(self):
        from apis.woocommerce_api.models.woocommerce_product_model import (
            WoocommerceProductModel,
        )

        return WoocommerceProductModel

    @property
    def woocommerce_brand_model(self):
        from apis.woocommerce_api.models.woocommerce_brand_model import WoocommerceBrandModel

        return WoocommerceBrandModel

    @property
    def woocommerce_category_model(self):
        from apis.woocommerce_api.models.woocommerce_category_model import (
            WoocommerceCategoryModel,
        )

        return WoocommerceCategoryModel

    @property
    def woocommerce_image_model(self):
        from apis.woocommerce_api.models.woocommerce_image_model import WoocommerceImageModel

        return WoocommerceImageModel

    # @property
    # def woocommerce_session_model(self):
    #     from apis.woocommerce_api.models.woocommerce_session_model import (
    #         WoocommerceSessionModel,
    #     )
    #     return WoocommerceSessionModel

    @property
    def woocommerce_tag_model(self):
        from apis.woocommerce_api.models.woocommerce_tag_model import WoocommerceTagModel

        return WoocommerceTagModel

    @property
    def woocommerce_tag_parser(self):
        from apis.woocommerce_api.services.woocommerce_tag_parser import WoocommerceTagParser

        return WoocommerceTagParser()

    @property
    def woocommerce_rollback(self):
        from apis.woocommerce_api.services.woocommerce_rollback import WoocommerceRollback

        return WoocommerceRollback()

    @property
    def woocommerce_uploader(self):
        from apis.woocommerce_api.services.woocommerce_uploader import WoocommerceUploader

        return WoocommerceUploader()

    @property
    def woocommerce_product(self):
        from apis.woocommerce_api.services.woocommerce_product import WoocommerceProduct

        return WoocommerceProduct()

    @property
    def woocommerce_brand(self):
        from apis.woocommerce_api.services.woocommerce_brand import WoocommerceBrand

        return WoocommerceBrand()

    @property
    def woocommerce_category(self):
        from apis.woocommerce_api.services.woocommerce_category import WoocommerceCategory

        return WoocommerceCategory()

    @property
    def woocommerce_image(self):
        from apis.woocommerce_api.services.woocommerce_image import WoocommerceImage

        return WoocommerceImage()

    @property
    def woocommerce_tag(self):
        from apis.woocommerce_api.services.woocommerce_tag import WoocommerceTag

        return WoocommerceTag()
