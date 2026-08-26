from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field, field_validator, model_validator


PROMPT_TEMPLATE = Path(__file__).with_name("prompt.txt").read_text(encoding="utf-8")


class SemanticSEO(BaseModel):
    german_title: str
    english_title: str
    german_description: str
    english_description: str
    german_short_description: str
    english_short_description: str
    german_meta_description: str
    english_meta_description: str
    focus_keywords: Annotated[list[str], Field(min_length=1, max_length=4)]
    primary_focus_keyword: str
    slug_components: Annotated[list[str], Field(min_length=5, max_length=5)]
    image_description: str
    product_tags: list[str]

    @field_validator("focus_keywords", "product_tags")
    @classmethod
    def unique_values(cls, values: list[str]) -> list[str]:
        result: list[str] = []
        for value in values:
            value = value.strip()
            if value and value not in result:
                result.append(value)
        return result

    @field_validator("slug_components")
    @classmethod
    def validate_slug_components(cls, values: list[str]) -> list[str]:
        if len(values) != 5:
            raise ValueError("slug_components must contain exactly 5 items")
        cleaned = [value.strip() for value in values]
        if any(not value for value in cleaned):
            raise ValueError("slug components cannot be empty")
        return cleaned

    @field_validator("image_description")
    @classmethod
    def validate_image_description(cls, value: str) -> str:
        if not 8 <= len(value.split()) <= 20:
            raise ValueError("image_description must contain 8 to 20 words")
        return value.strip()

    @model_validator(mode="after")
    def validate_primary_keyword(self) -> "SemanticSEO":
        if self.primary_focus_keyword not in self.focus_keywords:
            raise ValueError("primary_focus_keyword must exactly match one focus_keywords item")
        return self


class ProductInput(BaseModel):
    title: str = ""
    description: str = ""
    short_description: str = ""
    brand: str = ""
    condition: str = ""
    mpn: str = ""


class FinalSEO(BaseModel):
    title: str
    description: str
    short_description: str
    meta_description: str
    focus_keywords: list[str]
    primary_focus_keyword: str
    slug: str
    image_description: str
    product_tags: list[str]


GERMAN_ASCII_MAP = str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "Ä": "ae", "Ö": "oe", "Ü": "ue", "ß": "ss"})


def slugify_component(value: str) -> str:
    value = value.translate(GERMAN_ASCII_MAP).lower().strip()
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"[^a-z0-9-]+", "", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    if not value:
        raise ValueError("Slug component became empty")
    return value


def build_slug(components: list[str]) -> str:
    if len(components) != 5:
        raise ValueError(f"Expected exactly 5 semantic components, got {len(components)}")
    return "-".join(slugify_component(component) for component in components)


def keyword_links(keywords: list[str]) -> str:
    links = [f'<a href="/?s={keyword.replace(" ", "+")}">{keyword}</a>' for keyword in keywords]
    return "<h6>FOCUS KEYWORDS / SEO Keywords / Suchbegriffe</h6>" + ", ".join(links)


def assemble_final(semantic: SemanticSEO, product: ProductInput) -> FinalSEO:
    title = f"{semantic.german_title.strip()} | {semantic.english_title.strip()} | {product.condition.strip()}"

    paarmann_link = '<a href="https://www.paarmann-tech.de/shop/">Paarmann-Tech</a>'
    german_description = semantic.german_description.strip()
    if "Paarmann-Tech" not in german_description:
        german_description += f" Weitere technische Industrieprodukte finden Sie bei {paarmann_link}."

    description = f"<p>{german_description}</p><p>{semantic.english_description.strip()}</p>{keyword_links(semantic.focus_keywords)}"

    short_description = f"<p>{semantic.german_short_description.strip()}</p><p>{semantic.english_short_description.strip()}</p>"

    meta_description = f"{semantic.german_meta_description.strip()} | {semantic.english_meta_description.strip()}"

    final = FinalSEO(
        title=title,
        description=description,
        short_description=short_description,
        meta_description=meta_description,
        focus_keywords=semantic.focus_keywords,
        primary_focus_keyword=semantic.primary_focus_keyword,
        slug=build_slug(semantic.slug_components),
        image_description=semantic.image_description.strip(),
        product_tags=semantic.product_tags,
    )

    validate_final(final, product)
    return final


def validate_final(final: FinalSEO, product: ProductInput) -> None:
    if final.title.count(" | ") != 2:
        raise ValueError("Final title must contain exactly two separators")
    if not final.title.endswith(product.condition.strip()):
        raise ValueError("Condition must be final title element")
    if not 1 <= len(final.focus_keywords) <= 4:
        raise ValueError("focus_keywords must contain 1 to 4 items")
    if final.primary_focus_keyword not in final.focus_keywords:
        raise ValueError("Primary keyword missing from focus_keywords")
    if final.description.count("Paarmann-Tech") != 1:
        raise ValueError("Paarmann-Tech must appear exactly once")

    heading = "<h6>FOCUS KEYWORDS / SEO Keywords / Suchbegriffe</h6>"
    if heading not in final.description:
        raise ValueError("SEO keyword section missing")
    if not final.description.endswith(f">{final.focus_keywords[-1]}</a>"):
        raise ValueError("Description must end with final SEO keyword link")

    json.loads(final.model_dump_json())


def generate_semantic(
    product: ProductInput,
    *,
    model: str = "qwen3:8b",
    temperature: float = 0.2,
) -> SemanticSEO:
    prompt = PROMPT_TEMPLATE.format(**product.model_dump())

    from ollama import chat

    response = chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        format=SemanticSEO.model_json_schema(),
        options={"temperature": temperature},
    )

    return SemanticSEO.model_validate_json(response.message.content)


def generate_product(
    product: ProductInput,
    *,
    model: str = "qwen3:8b",
    temperature: float = 0.2,
) -> FinalSEO:
    semantic = generate_semantic(product, model=model, temperature=temperature)
    return assemble_final(semantic, product)


if __name__ == "__main__":
    example = ProductInput(
        title="Siemens SIMATIC S7-1200 CPU 1214C",
        description="Industrial controller. Model CPU 1214C.",
        short_description="Siemens automation controller.",
        brand="Siemens",
        condition="Gebraucht",
        mpn="",
    )

    result = generate_product(example)
    print(result.model_dump_json(indent=2))
