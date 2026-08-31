from bs4 import BeautifulSoup


class MatterhornSizeTableParser:
    ATTRIBUTE_NAMES = {
        "size": "Size",
        "underbust": "Underbust",
        "chest": "Chest",
    }

    # --
    # ...
    # --

    @classmethod
    def parse(cls, size_table_html: str) -> dict[str, list[str]]:

        if not size_table_html:
            return {}

        soup = BeautifulSoup(
            size_table_html,
            "html.parser",
        )

        table = soup.find("table")

        if not table:
            return {}

        headers = []

        header_row = table.find("tr")

        if not header_row:
            return {}

        for th in header_row.find_all("th"):
            header = th.get_text(strip=True)

            normalized = header.lower()

            attribute_name = cls.ATTRIBUTE_NAMES.get(normalized)

            if attribute_name:
                headers.append(attribute_name)
            else:
                headers.append(None)

        result = {attribute_name: [] for attribute_name in cls.ATTRIBUTE_NAMES.values()}

        for row in table.find_all("tr")[1:]:
            cells = row.find_all("td")

            if not cells:
                continue

            for index, cell in enumerate(cells):
                if index >= len(headers):
                    continue

                attribute_name = headers[index]

                if not attribute_name:
                    continue

                value = cell.get_text(
                    " ",
                    strip=True,
                )

                if not value:
                    continue

                if value not in result[attribute_name]:
                    result[attribute_name].append(value)

        return {key: values for key, values in result.items() if values}

    # --
    # ...
    # --

    @classmethod
    def parse_rows(
        cls,
        size_table_html: str,
    ) -> list[dict[str, str]]:

        if not size_table_html:
            return []

        soup = BeautifulSoup(
            size_table_html,
            "html.parser",
        )

        table = soup.find("table")

        if not table:
            return []

        header_row = table.find("tr")

        if not header_row:
            return []

        headers = []

        for th in header_row.find_all("th"):

            attribute_name = (
                cls.normalize_attribute_name(
                    th.get_text(
                        " ",
                        strip=True,
                    )
                )
            )

            headers.append(attribute_name)

        result = []

        for row in table.find_all("tr")[1:]:

            cells = row.find_all("td")

            if not cells:
                continue

            row_data = {}

            for index, cell in enumerate(cells):

                if index >= len(headers):
                    continue

                attribute_name = headers[index]

                if not attribute_name:
                    continue

                value = cell.get_text(
                    " ",
                    strip=True,
                )

                if not value:
                    continue

                row_data[attribute_name] = value

            if row_data:
                result.append(row_data)

        return result

    # --
    # ...
    # --

    @classmethod
    def parse_all(
        cls,
        size_table_html: str,
    ) -> dict:

        return {
            "attributes": cls.parse(
                size_table_html
            ),
            "rows": cls.parse_rows(
                size_table_html
            ),
        }