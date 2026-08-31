import time
from typing import Any

# --
# ...
# --


class SqlserverExecute:
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        try:
            self.db_command = kwargs.get("db_command")
            self.command = kwargs.get("command")
            self.sqlserver_connection = kwargs.get("sqlserver_connection")

            self.cursor = self.sqlserver_connection.cursor()

        except Exception as exp:
            self.error(f"{__file__}--->{__name__}: {exp!s}")

    #  --
    #  ...
    #  --

    def execute_db_command(self) -> Any:

        try:
            result: bool = True
            _ = 0

            self.info(self.db_command)

            self.cursor.execute(self.db_command)

            if len(self.cursor.messages) > 0:
                self.info(*list(map(lambda x: x, self.cursor.messages)))

            while self.cursor.nextset():
                self.info(f"I am yet {_} sec in SQLExecute...")
                time.sleep(5)
                _ += 5

        except Exception as exp:
            result = False
            self.error(f"{__file__}--->{__name__}: {exp!s}")

        finally:
            self.cursor.close()
            self.sqlserver_connection.close()
            return result

    #  --
    #  ...
    #  --

    def execute_command(self):

        try:
            result = {}
            commands = self.command.split(";")

            for command in commands:
                try:
                    self.info(command)
                    self.cursor.execute(command)

                    if len(self.cursor.messages) > 0:
                        self.info(*list(map(lambda x: x, self.cursor.messages)))

                    row = self.cursor.fetchone()
                    result = dict(zip(list(map(lambda x: x[0], row.cursor_description)), row))

                #  I have change this exp to bestimmt exception
                except Exception as exp:
                    self.error(f"{__file__}--->{__name__}: {exp!s}")

        except Exception as exp:
            self.error(f"{__file__}--->{__name__}: {exp!s}")
            result = "DB Fehler"

        finally:
            self.cursor.close()
            self.sqlserver_connection.close()
            return result
