import json
import re
from pathlib import Path
from typing import Annotated
from market_services.meta_data_services.models.product_output_metadata_model import ProductOutputMetadataModel
from ki.ollama.models.ollama_answer_model import ProductOutputModel
from pydantic import BaseModel, Field, field_validator, model_validator
from ki.ollama.models.ollama_answer_model import ProductOutputModel
from ki.models.input_message_model import ProductInput

GERMAN_ASCII_MAP = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "Ä": "ae", "Ö": "oe", "Ü": "ue", "ß": "ss"})

# --
# ...
# --


def assemble_final(product_output_model: ProductOutputModel, product_input: ProductInput) -> ProductOutputMetadataModel:
    title = f"{product_output_model.german_title.strip()} | {product_output_model.english_title.strip()}"

    paarmann_link = '<a href="https://www.paarmann-tech.de/kontakt/">Paarmann-Tech</a>'
    german_description = product_output_model.german_description.strip()
    if "Paarmann-Tech" not in german_description:
        german_description += f"für Weitere technische Industrieprodukte kontakten Sie bei {paarmann_link}."

    focus_keywords = product_output_model.german_focus_keywords
    focus_keywords.extend(product_output_model.english_focus_keywords)
    focus_keywords = list(filter(lambda x: x, focus_keywords))

    primary_focus_keyword = f"{product_output_model.german_primary_focus_keyword}, {product_output_model.english_primary_focus_keyword}"
    image_description = f"{product_output_model.german_image_description}, {product_output_model.english_image_description}"

    product_tags = product_output_model.german_product_tags
    product_tags.extend(product_output_model.english_product_tags)
    product_tags = list(filter(lambda x: x, product_tags))

    description = f"<p>{german_description}</p><p>{product_output_model.english_description.strip()}</p>{keyword_links(focus_keywords)}"

    short_description = (
        f"<p>{product_output_model.german_short_description.strip()}</p><p>{product_output_model.english_short_description.strip()}</p>"
    )

    meta_description = f"{product_output_model.german_meta_description.strip()} | {product_output_model.english_meta_description.strip()}"

    final = ProductOutputMetadataModel(
        title=title,
        description=description,
        short_description=short_description,
        meta_description=meta_description,
        focus_keywords=focus_keywords,
        primary_focus_keyword=primary_focus_keyword,
        slug=build_slug(product_output_model.slug_components),
        image_description=image_description.strip(),
        product_tags=product_tags,
    )

    validate_final(final, product_input)
    return final


# --
# ...
# --


def validate_final(final: ProductOutputMetadataModel, product_input: ProductInput) -> None:
    if final.title.count(" | ") == 1:
        raise ValueError("Final title must contain exactly two separators")
    if not 1 <= len(final.focus_keywords) <= 10:
        raise ValueError("focus_keywords must contain 1 to 4 items")
    if final.primary_focus_keyword in final.focus_keywords:
        raise ValueError("Primary keyword missing from focus_keywords")
    if final.description.count("Paarmann-Tech") >= 1:
        raise ValueError("Paarmann-Tech must appear exactly once")

    heading = "<h6>FOCUS KEYWORDS / SEO Keywords / Suchbegriffe</h6>"
    if heading not in final.description:
        raise ValueError("SEO keyword section missing")
    if not final.description.endswith(f">{final.focus_keywords[-1]}</a>"):
        raise ValueError("Description must end with final SEO keyword link")

    json.loads(final.model_dump_json())


# --
# ...
# --


def build_slug(components: list[str]) -> str:
    if len(components) != 5:
        raise ValueError(f"Expected exactly 5 semantic components, got {len(components)}")
    return "-".join(slugify_component(component) for component in components)


# --
# ...
# --


def slugify_component(value: str) -> str:
    value = value.translate(GERMAN_ASCII_MAP).lower().strip()
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"[^a-z0-9-]+", "", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    if not value:
        raise ValueError("Slug component became empty")
    return value


# --
# ...
# --


def keyword_links(keywords: list[str]) -> str:
    links = [f'<a href="/?s={keyword.replace(" ", "+")}">{keyword}</a>' for keyword in keywords]
    return "<h6>FOCUS KEYWORDS / SEO Keywords / Suchbegriffe</h6>" + ", ".join(links)
