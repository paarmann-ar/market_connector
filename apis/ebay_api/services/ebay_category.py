from apis.ebay_api.config.ebay_api_config import (
    EbayApiConfig,
)
from apis.ebay_api.core.base_ebay_api import BaseEbayApi
from apis.ebay_api.models.search_in_ebay_model import SearchInEbayModel
from apis.ebay_api.services.ebay_category_mapper import EbayCategoryMapper

# --
# ...
# --


class EbayCategory(BaseEbayApi):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.base_url = self.config_dictionary.get("base_url")
        self.taxonomy_url = self.config_dictionary.get("taxonomy_url")

        self.category_dict = {}

        self.ebay_token_api = kwargs.get("ebay_token_api", None)

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    #  --
    #  ...
    #  --

    @classmethod
    def get_config_dictionary(cls):
        return EbayApiConfig().get_dictionary()

    #  --
    #  ...
    #  --

    def get_default_category_tree_id_with_marketplace_id(self, marketplace):

        try:
            self.ebay_token_api.get_application_token()
            ebay_access_token = self.ebay_token_api.ebay_application_token

            response = self.request(
                method="get",
                url=f"{self.base_url}{self.taxonomy_url}/get_default_category_tree_id?marketplace_id={marketplace}",
                headers={
                    "Authorization": f"Bearer {ebay_access_token}",
                },
            )

            self.category_tree_id = int(response["categoryTreeId"])

            self.prompt_on_screen(f"Default category tree id: {self.category_tree_id}")

            return self.category_tree_id

        except Exception as exp:
            self.prompt_on_screen(f"get_default_category_tree_id_with_marketplace_id: {exp}")

    #  --
    #  ...
    #  --

    def get_category_tree(self, category_tree_id=""):

        try:
            if category_tree_id == "":
                category_tree_id = self.category_tree_id

            self.ebay_token_api.get_application_token()
            ebay_access_token = self.ebay_token_api.ebay_application_token

            response = self.request(
                method="get",
                url=f"{self.base_url}{self.taxonomy_url}/category_tree/{category_tree_id}",
                headers={
                    "Authorization": f"Bearer {ebay_access_token}",
                },
            )

            self.category_tree = response["rootCategoryNode"]

            return self.category_tree

        except Exception as exp:
            self.prompt_on_screen(f"get_category_tree: {exp}")

    #  --
    #  ...
    #  --

    def change_category_between_marketplaces(self, us_category_path):

        try:
            self.ebay_token_api.get_application_token()
            ebay_access_token = self.ebay_token_api.ebay_application_token

            ebay_category_mapper = EbayCategoryMapper(access_token=ebay_access_token)
            response = ebay_category_mapper.convert_us_category_path(us_category_path=us_category_path)

            return response

        except Exception as exp:
            self.prompt_on_screen(f"change_category_between_marketplaces: {exp}")

    #  --
    #  ...
    #  --

    def get_ebay_category_id(self, search_in_ebay_model: SearchInEbayModel) -> str:

        try:
            category_id_candidate = {}
            category_tree_id = self.get_default_category_tree_id_with_marketplace_id(marketplace=search_in_ebay_model.marketplace)

            if search_in_ebay_model.category_name_candidate:
                self.category_dict.clear()
                category_tree = self.get_category_tree(category_tree_id=category_tree_id)

                self.recursive_category(category_node=category_tree)

                for category_id, category_name in self.category_dict.items():
                    if category_name == search_in_ebay_model.category_name_candidate:
                        category_id_candidate[int(category_id)] = category_name

                self.prompt_on_screen(f"category id: {category_id_candidate}")

                search_in_ebay_model.category_id = category_id_candidate
                return category_id_candidate

            else:
                search_in_ebay_model.category_id = category_tree_id
                return {category_tree_id: "root"}

        except Exception as exp:
            self.prompt_on_screen(f"get_ebay_category_id: {exp}")

    #  --
    #  ...
    #  --

    def recursive_category(self, category_node: dict):
        if "childCategoryTreeNodes" not in category_node:
            self.category_dict.update({category_node["category"]["categoryId"]: category_node["category"]["categoryName"]})
            return

        for child in category_node["childCategoryTreeNodes"]:
            self.recursive_category(category_node=child)
