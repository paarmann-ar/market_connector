import html

from apis.woocommerce_api.config.woocommerce_api_config import (
    WoocommerceApiConfig,
)
from apis.woocommerce_api.core.base_woocommerce_api import (
    BaseWoocommerceApi,
)
from apis.woocommerce_api.models.woocommerce_category_model import (
    WoocommerceCategoryModel,
)
from slugify import slugify

# --
# ...
# --


class WoocommerceCategory(BaseWoocommerceApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.base_url = self.config_dictionary.get("base_url")
        self.wp_media_url = self.config_dictionary.get("wp_media_url")

        self.consumer_key = self.config_dictionary.get("consumer_key")
        self.consumer_secret = self.config_dictionary.get("consumer_secret")

        self.wp_user = self.config_dictionary.get("wp_user")
        self.wp_password = self.config_dictionary.get("wp_password")

        self.category_url = self.config_dictionary.get("category_url")

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return WoocommerceApiConfig().get_dictionary()

    # --
    # ...
    # --

    def __call__(self, category_id) -> str:
        pass

    # --
    # ...
    # --

    def sync_categories(
        self,
        categories: list[WoocommerceCategoryModel]
    ) -> dict[str, WoocommerceCategoryModel]:

        category_index = self.build_category_index(categories)

        synced_categories: dict[str, WoocommerceCategoryModel] = {}

        sorted_categories = sorted(
            category_index.values(),
            key=lambda category: len(
                self.normalize_path(category.path)
            ),
        )

        for category in sorted_categories:

            parent_path = self.get_parent_path(category.path)

            if parent_path:
                parent = synced_categories.get(parent_path)

                if not parent:
                    raise ValueError(
                        f"Parent category not synced: {parent_path}"
                    )

                category.parent_id = parent.id

            else:
                category.parent_id = None

            synced_category = self.resolve_or_upload(category)

            synced_categories[category.path] = synced_category

        return synced_categories

    # --
    # ...
    # --

    def get_category_by_name(
        self,
        name: str,
        parent_id: int = 0,
        record_per_page: int = 100
    ):
        response = self.request(
            method="get",
            url=f"{self.base_url}{self.category_url}",
            auth=(self.consumer_key, self.consumer_secret),
            params={
                "per_page": record_per_page,
            },
        )

        if not response:
            return None

        normalized_name = html.unescape(name).strip().lower()

        for category in response:
            category_name = html.unescape(
                category["name"]
            ).strip().lower()

            if category_name != normalized_name:
                continue

            if category.get("parent", 0) != parent_id:
                continue

            return WoocommerceCategoryModel.from_api(category)

        return None

    # --
    # ...
    # --

    def get_all_categories(self, record_per_page: int = 100):

        try:
            response = self.request(
                method="get",
                url=f"{self.base_url}{self.category_url}",
                auth=(self.consumer_key, self.consumer_secret),
                params={"per_page": record_per_page},
            )

            self.prompt_on_screen(f"categories: {response}")

        except Exception as exp:
            self.prompt_on_screen(f"get_all_categories: {exp}")

    # --
    # ...
    # --

    def upload_category(self, category_model: WoocommerceCategoryModel):

        try:
            response = self.request(
                method="post",
                url=f"{self.base_url}{self.category_url}",
                auth=(self.consumer_key, self.consumer_secret),
                json=category_model.to_dict(),
            )

            self.prompt_on_screen(f"categoriey to upload: {response}")

            woocommerce_category_model = WoocommerceCategoryModel.from_api(response)
            return woocommerce_category_model

        except Exception as exp:
            self.prompt_on_screen(f"upload_category: {exp}")

    # --
    # ...
    # --

    def resolve_or_upload(
        self,
        category: WoocommerceCategoryModel,
    ) -> WoocommerceCategoryModel:

        if not category.path:
            parent_id = category.parent_id or 0

            existing = self.get_category_by_name(
                name=category.name,
                parent_id=parent_id,
            )

            if existing:
                return existing

            return self.upload_category(category)

        return self.resolve_or_upload_path(category.path)

    # --
    # ...
    # --

    def resolve_or_upload_path(
        self,
        path: str,
    ) -> WoocommerceCategoryModel:

        parts = self.normalize_path(path)

        parent_id = 0
        current_path_parts = []

        for name in parts:

            current_path_parts.append(name)

            current_path = self.build_path(
                current_path_parts
            )

            category = WoocommerceCategoryModel(
                name=name,
                slug=slugify(name),
                path=current_path,
                parent_id=parent_id or None,
            )

            category = self.resolve_or_upload_single(
                category
            )

            parent_id = category.id

        return category

    # --
    # ...
    # --

    def resolve_or_upload_single(
        self,
        category: WoocommerceCategoryModel,
    ) -> WoocommerceCategoryModel:

        parent_id = category.parent_id or 0

        existing = self.get_category_by_name(
            name=category.name,
            parent_id=parent_id,
        )

        if existing:
            return existing

        return self.upload_category(category)

    # --
    # ...
    # --

    def delete_category_by_category_id(self, category_id: int):

        try:
            response = self.request(
                method="delete",
                url=f"{self.base_url}{self.category_url}/{category_id}",
                auth=(self.consumer_key, self.consumer_secret),
                params={"force": True},
            )

            self.prompt_on_screen(f"category deleted: {response}")

            return response

        except Exception as exp:
            self.prompt_on_screen(f"delete_category_by_category_id: {exp}")

    # --
    # ...
    # --


    @staticmethod
    def normalize_path(path: str) -> list[str]:
        return [
            part.strip()
            for part in path.strip("/").split("/")
            if part.strip()
        ]
    
    # --
    # ...
    # --

    @staticmethod
    def build_path(parts: list[str]) -> str:
        return "/" + "/".join(parts)

    # --
    # ...
    # --


    @staticmethod
    def get_parent_path(path: str) -> str | None:
        parts = WoocommerceCategory.normalize_path(path)

        if len(parts) <= 1:
            return None

        return WoocommerceCategory.build_path(parts[:-1])
    
    # --
    # ...
    # --

    @staticmethod
    def build_category_index(
        categories: list[WoocommerceCategoryModel],
    ) -> dict[str, WoocommerceCategoryModel]:

        result: dict[str, WoocommerceCategoryModel] = {}

        for category in categories:

            if not category.path:
                continue

            parts = WoocommerceCategory.normalize_path(
                category.path
            )

            for i, name in enumerate(parts):

                path = WoocommerceCategory.build_path(
                    parts[: i + 1]
                )

                if path not in result:
                    result[path] = WoocommerceCategoryModel(
                        name=name,
                        slug=slugify(name),
                        path=path,
                    )

        return result

    @staticmethod
    def resolve_parent(
        category: WoocommerceCategoryModel,
        category_index: dict[str, WoocommerceCategoryModel],
    ) -> WoocommerceCategoryModel | None:

        if not category.path:
            return None

        parent_path = WoocommerceCategory.get_parent_path(
            category.path
        )

        if parent_path is None:
            return None

        return category_index.get(parent_path)
