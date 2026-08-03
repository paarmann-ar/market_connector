import CONSTS
from services.core.base import Base
from services.disk.file.config.file_config import FileConfig

# --
# ...
# --


class FileManager(Base):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.mode = self.config_dictionary["mode"]
        self.address = f"{CONSTS.ROOT_DIR}/{self.config_dictionary['address']}"

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return FileConfig().get_dictionary()

    # --
    # ...
    # --

    def operation(self, mode="", address="", context="", output="row") -> str:

        try:
            if mode == "":
                mode = self.mode

            if address == "":
                address = self.address

            match mode:
                case "r":
                    with open(address, mode) as file:
                        context = file.read()

                        match output:
                            case "list":
                                context = context.split("\n")

                case "w":
                    with open(address, mode) as file:
                        file.write(context)

                case "a":
                    with open(address, mode) as file:
                        file.write(context)

                case _:
                    with open(address, mode) as file:
                        file.write(context)

        # I have change this exp to bestimmt
        except FileNotFoundError as exp:
            print(repr(exp))

        except Exception as exp:
            print(repr(exp))

        finally:
            pass

        return context
