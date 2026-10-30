from html import escape
from apis.ebay_api.models.browse.product_ebay_model import ProductEbayModel

# --
# ...
# --


class TechnicalTableBuilder:
    # --
    # ...
    # --

    @staticmethod
    def build(
        technical_attributes: dict[str, str] | None,
        brand: str | None = None,
        mpn: str | None = None,
        condition: str | None = None,
        gtin: str | None = None,
        language: str = "en",
    ) -> str:

        rows: list[tuple[str, str]] = []
        seen: set[str] = set()

        def add_row(label: str, value: str | None) -> None:
            if value is None:
                return

            label = str(label).strip()
            value = str(value).strip()

            if not label or not value:
                return

            key = label.casefold()

            if key in seen:
                return

            seen.add(key)
            rows.append((label, value))

        # -----------------------------------------
        # Core product information
        # -----------------------------------------

        if language == "de":
            add_row("Marke", brand)
            add_row("MPN", mpn)
            add_row("Zustand", condition)
        else:
            add_row("Brand", brand)
            add_row("MPN", mpn)
            add_row("Condition", condition)

        # GTIN only if you really want it in the table
        add_row("GTIN", gtin)

        # -----------------------------------------
        # Technical attributes
        # -----------------------------------------

        for name, value in (technical_attributes or {}).items():
            add_row(name, value)

        if not rows:
            return ""

        # -----------------------------------------
        # Headers
        # -----------------------------------------

        if language == "de":
            specification_header = "Technische Eigenschaft"
            value_header = "Wert"
        else:
            specification_header = "Technical Specification"
            value_header = "Value"

        # -----------------------------------------
        # HTML rows
        # -----------------------------------------

        html_rows = "\n".join((f"        <tr><td>{escape(label)}</td><td>{escape(value)}</td></tr>") for label, value in rows)

        # -----------------------------------------
        # Real HTML table
        # -----------------------------------------

        return f"""
                <table class="technical-specifications" style="width:100%; border-collapse:collapse; margin:20px 0;">
                    <thead>
                        <tr>
                            <th style="text-align:left; padding:10px; border:1px solid #ddd;">
                                {escape(specification_header)}
                            </th>
                            <th style="text-align:left; padding:10px; border:1px solid #ddd;">
                                {escape(value_header)}
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                {html_rows}
                    </tbody>
                </table>
                """.strip()

    # --
    # ...
    # --

    def get_technical_attributes(
        self,
        product_ebay_model: ProductEbayModel,
    ) -> dict[str, str]:

        aspects = product_ebay_model.aspects or product_ebay_model.localizedAspects or []

        excluded_names = {
            "brand",
            "mpn",
            "manufacturer",
            "condition",
        }

        technical_attributes: dict[str, str] = {}
        seen: set[str] = set()

        for aspect in aspects:
            name = aspect.get("name")
            value = aspect.get("value")

            if not name or value is None:
                continue

            name = str(name).strip()
            value = str(value).strip()

            if not name or not value:
                continue

            normalized_name = name.casefold()

            if normalized_name in excluded_names:
                continue

            if normalized_name in seen:
                continue

            seen.add(normalized_name)
            technical_attributes[name] = value

        return technical_attributes
