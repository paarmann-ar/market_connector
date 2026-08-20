from __future__ import annotations

from typing import Any, Optional

import requests


class EbayCategoryMapper:
    """
    Convert an eBay US category path to an eBay DE category.

    Input example:

        12576|183978|184112|184148

    or:

        12576 > 183978 > 184112 > 184148

    Output:

        {
            "de_cat_id": "12345",
            "de_cat_path": "100 > 200 > 300 > 12345",
            "de_cat_name_path": (
                "Business & Industrie > "
                "Hydraulik > "
                "Ventile > "
                "Druckventile"
            )
        }

    Important:
        - Taxonomy API uses an Application Access Token.
        - US and DE have different category trees.
        - US category IDs are NOT directly converted to DE IDs.
        - We first resolve the US category name.
        - Then we search the DE taxonomy.
    """

    BASE_URL = "https://api.ebay.com"

    TAXONOMY_BASE_URL = f"{BASE_URL}/commerce/taxonomy/v1"

    def __init__(
        self,
        access_token: str,
        timeout: tuple[int, int] = (12, 120),
    ) -> None:

        if not access_token:
            raise ValueError("eBay application access token is required.")

        self.access_token = access_token
        self.timeout = timeout

        self.session = requests.Session()

        self.session.headers.update(
            {
                "Authorization": (f"Bearer {access_token}"),
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

        self._category_tree_cache: dict[
            str,
            str,
        ] = {}

    # =========================================================
    # HTTP
    # =========================================================

    def _get(
        self,
        url: str,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:

        response = self.session.get(
            url,
            params=params,
            timeout=self.timeout,
        )

        if response.status_code >= 400:
            print("\n================================")

            print("EBAY CATEGORY ERROR")

            print(
                "STATUS:",
                response.status_code,
            )

            print(
                "URL:",
                response.url,
            )

            print(
                "TEXT:",
                response.text,
            )

            print("================================\n")

            response.raise_for_status()

        return response.json()

    # =========================================================
    # PARSE CATEGORY PATH
    # =========================================================

    @staticmethod
    def parse_category_path(
        category_path: str,
    ) -> list[str]:

        if not category_path:
            raise ValueError("category_path cannot be empty.")

        value = str(category_path).strip()

        # Support:
        #
        # 12576|183978|184112|184148
        #
        # 12576 > 183978 > 184112 > 184148
        #
        # 12576/183978/184112/184148

        value = value.replace(">", "|").replace("/", "|").replace("\\", "|")

        category_ids = [item.strip() for item in value.split("|") if item.strip()]

        if not category_ids:
            raise ValueError(f"Invalid category path: {category_path}")

        return category_ids

    # =========================================================
    # GET LEAF CATEGORY ID
    # =========================================================

    def get_leaf_category_id(
        self,
        category_path: str,
    ) -> str:

        category_ids = self.parse_category_path(category_path)

        return category_ids[-1]

    # =========================================================
    # GET DEFAULT CATEGORY TREE ID
    # =========================================================

    def get_default_category_tree_id(
        self,
        marketplace_id: str,
    ) -> str:

        marketplace_id = marketplace_id.strip().upper()

        if marketplace_id in (self._category_tree_cache):
            return self._category_tree_cache[marketplace_id]

        url = f"{self.TAXONOMY_BASE_URL}/get_default_category_tree_id"

        response = self._get(
            url,
            params={
                "marketplace_id": marketplace_id,
            },
        )

        category_tree_id = response.get("categoryTreeId")

        if category_tree_id is None:
            raise ValueError(f"eBay did not return categoryTreeId.\nResponse: {response}")

        category_tree_id = str(category_tree_id)

        self._category_tree_cache[marketplace_id] = category_tree_id

        print(
            f"{marketplace_id} CATEGORY TREE ID:",
            category_tree_id,
        )

        return category_tree_id

    # =========================================================
    # GET CATEGORY SUBTREE
    # =========================================================

    def get_category_subtree(
        self,
        marketplace_id: str,
        category_id: str,
    ) -> dict[str, Any]:

        marketplace_id = marketplace_id.strip().upper()

        tree_id = self.get_default_category_tree_id(marketplace_id)

        url = f"{self.TAXONOMY_BASE_URL}/category_tree/{tree_id}/get_category_subtree"

        print("\nGET CATEGORY SUBTREE")

        print(
            "Marketplace:",
            marketplace_id,
        )

        print(
            "Tree ID:",
            tree_id,
        )

        print(
            "Category ID:",
            category_id,
        )

        return self._get(
            url,
            params={
                "category_id": str(category_id),
            },
        )

    # =========================================================
    # FIND CATEGORY NODE RECURSIVELY
    # =========================================================

    @staticmethod
    def find_category_node(
        node: dict[str, Any],
        category_id: str,
    ) -> Optional[dict[str, Any]]:

        category = node.get("category") or {}

        current_id = category.get("categoryId")

        if current_id is not None and str(current_id) == str(category_id):
            return node

        children = node.get("childCategoryTreeNodes") or []

        for child in children:
            result = EbayCategoryMapper.find_category_node(
                child,
                category_id,
            )

            if result is not None:
                return result

        return None

    # =========================================================
    # FIND CATEGORY IN SUBTREE RESPONSE
    # =========================================================

    @classmethod
    def find_category_in_subtree(
        cls,
        response: dict[str, Any],
        category_id: str,
    ) -> Optional[dict[str, Any]]:

        # eBay get_category_subtree response:
        #
        # {
        #     "categoryTreeId": "0",
        #     "categoryTreeVersion": "...",
        #     "categorySubtreeNode": {
        #         ...
        #     }
        # }

        root = response.get("categorySubtreeNode")

        if not root:
            return None

        return cls.find_category_node(
            root,
            category_id,
        )

    # =========================================================
    # GET US CATEGORY NAME
    # =========================================================

    def get_us_category_name(
        self,
        us_category_path: str,
    ) -> str:

        category_ids = self.parse_category_path(us_category_path)

        leaf_id = category_ids[-1]

        print("\n================================")

        print("US CATEGORY")

        print("================================")

        print(
            "US PATH:",
            us_category_path,
        )

        print(
            "US IDS:",
            category_ids,
        )

        print(
            "US LEAF:",
            leaf_id,
        )

        response = self.get_category_subtree(
            marketplace_id="EBAY_US",
            category_id=leaf_id,
        )

        node = self.find_category_in_subtree(
            response,
            leaf_id,
        )

        if node is None:
            # -------------------------------------------------
            # Important:
            #
            # eBay may return the requested category as
            # rootCategoryNode instead of a child node.
            # We already search recursively above.
            #
            # If it is still not found, fail with useful
            # debugging information.
            # -------------------------------------------------

            root = response.get("rootCategoryNode")

            root_category = root.get("category", {}) if root else {}

            raise ValueError(
                "US category was not found "
                "in eBay taxonomy.\n"
                f"Requested ID: {leaf_id}\n"
                f"Root category: "
                f"{root_category}\n"
                f"Response keys: "
                f"{list(response.keys())}"
            )

        category = node.get("category") or {}

        category_name = category.get("categoryName")

        if not category_name:
            raise ValueError(f"US category exists but categoryName is missing.\nCategory: {category}")

        print(
            "US CATEGORY ID:",
            category.get("categoryId"),
        )

        print(
            "US CATEGORY NAME:",
            category_name,
        )

        return str(category_name)

    # =========================================================
    # GET CATEGORY SUGGESTIONS
    # =========================================================

    def get_category_suggestions(
        self,
        marketplace_id: str,
        query: str,
    ) -> list[dict[str, Any]]:

        marketplace_id = marketplace_id.strip().upper()

        tree_id = self.get_default_category_tree_id(marketplace_id)

        url = f"{self.TAXONOMY_BASE_URL}/category_tree/{tree_id}/get_category_suggestions"

        print("\nGET CATEGORY SUGGESTIONS")

        print(
            "Marketplace:",
            marketplace_id,
        )

        print(
            "Query:",
            query,
        )

        response = self._get(
            url,
            params={
                "q": query,
            },
        )

        return response.get(
            "categorySuggestions",
            [],
        )

    # =========================================================
    # BUILD NUMERIC PATH
    # =========================================================

    @staticmethod
    def build_numeric_path(
        suggestion: dict[str, Any],
    ) -> str:

        category = suggestion.get("category") or {}

        ancestors = suggestion.get("categoryTreeNodeAncestors") or []

        path: list[str] = []

        for ancestor in reversed(ancestors):
            category_id = ancestor.get("categoryId")

            if category_id:
                path.append(str(category_id))

        category_id = category.get("categoryId")

        if category_id:
            path.append(str(category_id))

        return " > ".join(path)

    # =========================================================
    # BUILD NAME PATH
    # =========================================================

    @staticmethod
    def build_name_path(
        suggestion: dict[str, Any],
    ) -> str:

        category = suggestion.get("category") or {}

        ancestors = suggestion.get("categoryTreeNodeAncestors") or []

        path: list[str] = []

        for ancestor in reversed(ancestors):
            name = ancestor.get("categoryName")

            if name:
                path.append(str(name))

        category_name = category.get("categoryName")

        if category_name:
            path.append(str(category_name))

        return " > ".join(path)

    # =========================================================
    # FIND DE CATEGORY
    # =========================================================

    def find_de_category(
        self,
        query: str,
    ) -> dict[str, Any]:

        suggestions = self.get_category_suggestions(
            marketplace_id="EBAY_DE",
            query=query,
        )

        if not suggestions:
            raise ValueError(f"No DE category suggestion found for query: {query}")

        print(
            "\nDE CATEGORY SUGGESTIONS:",
            len(suggestions),
        )

        # -------------------------------------------------
        # For now select eBay's first / best suggestion.
        # -------------------------------------------------

        best = suggestions[0]

        category = best.get("category") or {}

        de_cat_id = category.get("categoryId")

        de_cat_name = category.get("categoryName")

        if not de_cat_id:
            raise ValueError(f"DE suggestion does not contain categoryId.\nSuggestion: {best}")

        print(
            "DE CATEGORY ID:",
            de_cat_id,
        )

        print(
            "DE CATEGORY NAME:",
            de_cat_name,
        )

        return {
            "suggestion": best,
            "de_cat_id": str(de_cat_id),
            "de_cat_name": (str(de_cat_name) if de_cat_name else ""),
        }

    # =========================================================
    # MAIN METHOD
    # =========================================================

    def convert_us_category_path(
        self,
        us_category_path: str,
    ) -> dict[str, str]:

        print("\n================================")

        print("US -> DE CATEGORY CONVERSION")

        print("================================")

        print(
            "INPUT US PATH:",
            us_category_path,
        )

        # -------------------------------------------------
        # 1. Parse US path
        # -------------------------------------------------

        us_category_ids = self.parse_category_path(us_category_path)

        print(
            "US CATEGORY IDS:",
            us_category_ids,
        )

        us_leaf_id = us_category_ids[-1]

        print(
            "US LEAF ID:",
            us_leaf_id,
        )

        # -------------------------------------------------
        # 2. Get US category name
        # -------------------------------------------------

        us_category_name = self.get_us_category_name(us_category_path)

        # -------------------------------------------------
        # 3. Search DE taxonomy
        # -------------------------------------------------

        de_result = self.find_de_category(query=us_category_name)

        suggestion = de_result["suggestion"]

        # -------------------------------------------------
        # 4. Extract DE category ID
        # -------------------------------------------------

        de_cat_id = de_result["de_cat_id"]

        # -------------------------------------------------
        # 5. Build DE numeric path
        # -------------------------------------------------

        de_cat_path = self.build_numeric_path(suggestion)

        # -------------------------------------------------
        # 6. Build DE name path
        # -------------------------------------------------

        de_cat_name_path = self.build_name_path(suggestion)

        # -------------------------------------------------
        # 7. Validate result
        # -------------------------------------------------

        if not de_cat_path:
            raise ValueError(f"DE category path is empty.\nSuggestion: {suggestion}")

        if not de_cat_name_path:
            raise ValueError(f"DE category name path is empty.\nSuggestion: {suggestion}")

        # -------------------------------------------------
        # 8. Final result
        # -------------------------------------------------

        result = {
            "de_cat_id": de_cat_id,
            "de_cat_path": de_cat_path,
            "de_cat_name_path": (de_cat_name_path),
        }

        print("\n================================")

        print("FINAL RESULT")

        print("================================")

        print(
            "de_cat_id:",
            result["de_cat_id"],
        )

        print(
            "de_cat_path:",
            result["de_cat_path"],
        )

        print(
            "de_cat_name_path:",
            result["de_cat_name_path"],
        )

        print("================================\n")

        return result
