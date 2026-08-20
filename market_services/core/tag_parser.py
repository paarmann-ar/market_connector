import re

from apis.woocommerce_api.models.woocommerce_tag_parser_model import (
    WoocommerceTagParserModel,
)
from market_services.core.tag_constants import (
    BRANDS,
    CATEGORIES,
    CONDITIONS,
    NO_GO_WORDS,
)

# --
# ...
# --


class TagParser:
    BRANDS = BRANDS
    CONDITIONS = CONDITIONS
    CATEGORIES = CATEGORIES
    NO_GO_WORDS = NO_GO_WORDS

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    # --
    # ...
    # --

    def __call__(self, context: str) -> str:
        self.tag_parser(context)

    # --
    # ...
    # --

    def tag_parser(self, context: str) -> WoocommerceTagParserModel:

        brand = self.find_brand(context)
        condition = self.find_condition(context)
        part_numbers = self.find_part_number(context)
        category = self.find_category(context)

        clean_name = self.clean_title(context, brand, condition, part_numbers, category)

        tags = self.build_tags(
            name=clean_name,
            brand=brand,
            part_numbers=part_numbers,
            catgory=category,
            condition=condition,
        )

        return WoocommerceTagParserModel(
            name=clean_name,
            brand=brand,
            condition=condition,
            part_number=part_numbers,
            category=category,
            tags=tags,
        )

    # --
    # ...
    # --

    def normalize_context(self, context: str):

        context = context.lower()
        context = re.sub(r"[^a-z0-9äöüß\- ]", " ", context)
        context = re.sub(r"\s+", " ", context)

        return context.strip()

    # --
    # ...
    # --

    def find_brand(self, context: str):
        context = self.normalize_context(context)

        for brand in self.BRANDS:
            if brand.lower() in context.lower():
                return brand

        return None

    # --
    # ...
    # --

    def find_category(self, context: str):
        context = self.normalize_context(context)

        for category in self.CATEGORIES:
            if category.lower() in context.lower():
                return category

        return None

    # --
    # ...
    # --

    def find_condition(self, context: str):
        context = self.normalize_context(context)

        for condition in self.CONDITIONS:
            if condition.lower() in context.lower():
                return condition

        return None

    # --
    # ...
    # --

    def find_part_number(self, context: str):

        context = self.normalize_context(context)

        patterns = [
            r"\b[A-Z]{2,}\d+[A-Z0-9-]*\b",
            r"\b6ES\d+[A-Z0-9-]*\b",
            r"\b6ES\d+\s+\d+[A-Z0-9-]*\b",
        ]

        matches = []

        for pattern in patterns:
            matches.extend(re.findall(pattern, context, re.I))

        return list(dict.fromkeys(matches))

    # --
    # ...
    # --

    def clean_title(self, context: str, brand, condition, part_numbers: list, category):

        try:
            result = context

            remove_words = [brand, condition, category]
            remove_words.extend(part_numbers)

            for word in remove_words:
                if word:
                    result = result.lower().replace(word.lower(), "")

            for no_go_word in self.NO_GO_WORDS:
                result = result.replace(no_go_word, "")

            return " ".join(result.split()).strip()

        except Exception as exp:
            self.prompt_on_screen(f"clean_title: {exp}")

    # --
    # ...
    # --

    def build_tags(self, name, brand, part_numbers, catgory, condition):

        try:
            tags: list[str] = []

            if name:
                if isinstance(name, list):
                    tags.extend(name)
                else:
                    tags.append(name)

            if brand:
                if isinstance(brand, list):
                    tags.extend(brand)
                else:
                    tags.append(brand)

            if part_numbers:
                if isinstance(part_numbers, list):
                    tags.extend(part_numbers)
                else:
                    tags.append(part_numbers)

            if catgory:
                if isinstance(catgory, list):
                    tags.extend(catgory)
                else:
                    tags.append(catgory)

            if condition:
                if isinstance(condition, list):
                    tags.extend(condition)
                else:
                    tags.append(condition)

            for i, tag in enumerate(tags):
                tags[i] = tag.replace("|", "").strip()

            return tags

        except Exception as exp:
            self.prompt_on_screen(f"build_tags: {exp}")
