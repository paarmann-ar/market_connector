from __future__ import annotations

import unittest

from seo_pipeline import ProductInput, SemanticSEO, assemble_final, build_slug


class PipelineTests(unittest.TestCase):
    def test_slug_from_exactly_five_semantic_inputs(self) -> None:
        self.assertEqual(
            build_slug(["Siemens", "SIMATIC", "S7-1200", "CPU", "1214C"]),
            "siemens-simatic-s7-1200-cpu-1214c",
        )

    def test_assembler_forces_bilingual_fields(self) -> None:
        product = ProductInput(
            title="Siemens SIMATIC S7-1200 CPU 1214C",
            condition="Gebraucht",
        )

        semantic = SemanticSEO(
            german_title="Siemens SIMATIC Steuerung CPU 1214C",
            english_title="Siemens SIMATIC Controller CPU 1214C",
            german_description="Technische Beschreibung.",
            english_description="Technical description.",
            german_short_description="Kurze Beschreibung.",
            english_short_description="Short description.",
            german_meta_description="Siemens SIMATIC Steuerung CPU 1214C.",
            english_meta_description="Siemens SIMATIC controller CPU 1214C.",
            focus_keywords=["Siemens SIMATIC Steuerung"],
            primary_focus_keyword="Siemens SIMATIC Steuerung",
            slug_components=["Siemens", "SIMATIC", "S7-1200", "CPU", "1214C"],
            image_description="Siemens SIMATIC S7-1200 industrial controller CPU 1214C front product view",
            product_tags=["Siemens", "SIMATIC S7-1200", "CPU 1214C"],
        )

        final = assemble_final(semantic, product)

        self.assertIn(" | ", final.title)
        self.assertIn("<p>Technische Beschreibung.", final.description)
        self.assertIn("<p>Technical description.</p>", final.description)
        self.assertEqual(final.slug, "siemens-simatic-s7-1200-cpu-1214c")


if __name__ == "__main__":
    unittest.main()
