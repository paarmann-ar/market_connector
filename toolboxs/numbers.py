from decimal import Decimal


class Numbers:
    @staticmethod
    def price_anpassen(prise: str, price_anpassen) -> str:

        price = round(Decimal(str(prise)) * Decimal(str(price_anpassen)))

        return str(price)
