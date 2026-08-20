import re


class CleanProductDescription:
    # Sections that usually indicate non-product information.
    REMOVE_SECTION_PATTERNS = [
        # German
        r"\bBEZAHLUNG\b",
        r"\bVERSAND\b",
        r"\bZAHLUNG\s*&\s*VERSAND\b",
        r"\bÜBER\s+UNS\b",
        r"\bKONTAKTIEREN\s+SIE\s+UNS\b",
        r"\bRÜCKNAHMEN\b",
        r"\bRÜCKGABE\b",
        r"\bRÜCKSENDUNG\b",
        r"\bERSTATTUNG\b",
        r"\bGARANTIE\b",
        r"\bZAHLUNGSBEDINGUNGEN\b",
        r"\bVERSANDKOSTEN\b",
        r"\bVERSAND\s+NACH\s+ZAHLUNG\b",
        r"\bLIEFERZEIT\b",
        r"\bLIEFERADRESSE\b",
        r"\bKÄUFER\b",
        r"\bKUNDE\b",
        r"\bZOLL\b",
        r"\bZÖLLE\b",
        r"\bZOLLGEBÜHREN\b",
        r"\bEINFUHRZÖLLE\b",
        r"\bMEHRWERTSTEUER\b",
        r"\bMWST\.?\b",
        r"\bSTEUERN\b",
        r"\bRECHNUNG\b",
        r"\bRECHNUNGEN\b",
        r"\bVERPACKUNG\b",
        r"\bKONTAKT\b",
        r"\bE-MAIL\b",
        r"\bTELEFON\b",
        # English
        r"\bABOUT\s+US\b",
        r"\bCONTACT\s+US\b",
        r"\bSHIPPING\b",
        r"\bDELIVERY\b",
        r"\bDELIVERY\s+TIME\b",
        r"\bSHIPPING\s+ADDRESS\b",
        r"\bSHIPPING\s+COST\b",
        r"\bPAYMENT\b",
        r"\bPAYMENT\s+TERMS\b",
        r"\bPAYMENT\s+RECEIVED\b",
        r"\bRETURN\b",
        r"\bREFUND\b",
        r"\bWARRANTY\b",
        r"\bCUSTOMS\b",
        r"\bCUSTOMS\s+DUTIES\b",
        r"\bIMPORT\s+DUTIES\b",
        r"\bBUYER\b",
        r"\bPURCHASER\b",
        r"\bCUSTOMER\b",
        r"\bCONTACT\s+INFORMATION\b",
        r"\bPHONE\s+NUMBER\b",
        r"\bEMAIL\s+ADDRESS\b",
        r"\bWEBSITE\b",
        r"\bSUPPORT\b",
        # Generic eBay / seller content
        r"\bMANY\s+MORE\s+ITEMS\b",
        r"\bMORE\s+AUCTIONS\s+IN\s+OUR\s+SHOP\b",
        r"\bOTHER\s+GENERIC\s+COMPANY\s+INFORMATION\b",
    ]

    @classmethod
    def clean_product_description(cls, text: str) -> str:

        if not text:
            return ""

        if not isinstance(text, str):
            text = str(text)

        cleaned_text = text

        # Normalize whitespace first.
        cleaned_text = re.sub(
            r"\r\n|\r",
            "\n",
            cleaned_text,
        )

        # Remove everything from the first matching
        # non-product section until the end.
        for pattern in cls.REMOVE_SECTION_PATTERNS:
            match = re.search(
                pattern,
                cleaned_text,
                flags=re.IGNORECASE,
            )

            if match:
                cleaned_text = cleaned_text[: match.start()]

        # Remove excessive whitespace.
        cleaned_text = re.sub(
            r"[ \t]+",
            " ",
            cleaned_text,
        )

        # Remove excessive empty lines.
        cleaned_text = re.sub(
            r"\n{3,}",
            "\n\n",
            cleaned_text,
        )

        return cleaned_text.strip()
