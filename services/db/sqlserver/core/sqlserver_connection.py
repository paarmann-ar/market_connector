from typing import Any

import pyodbc

# --
# ...
# --


class SqlserverConnection:
    # --
    # ...
    # --

    @classmethod
    def create_connection_string(cls, **kwargs) -> str:

        try:
            return f"""DRIVER={{{kwargs.get("driver")}}};server={kwargs.get("host")};database={kwargs.get("database")};trusted_connection=yes;uid={kwargs.get("username")};pwd={kwargs.get("password")};"""

        except Exception as exp:
            cls.error(f"{__file__}--->{__name__}: {exp!s}")

    # --
    # ...
    # --

    @classmethod
    def get_connection(cls, connection_string: str) -> Any:

        try:
            return pyodbc.connect(connection_string, autocommit=True)

        except Exception as exp:
            cls.error(f"{__file__}--->{__name__}: {exp!s}")
