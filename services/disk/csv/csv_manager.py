import pandas

import CONSTS
from services.disk.core.base_disk import BaseDisk
from services.disk.csv.config.csv_config import CSVConfig

# --
# ...
# --


class CSVManager(BaseDisk):
    def __init__(self, **kwargs) -> None:
        super().__init__()

        self.mode = kwargs.get("mode", self.instance.config_dictionary["default_mode"])
        self.address = kwargs.get(
            "address",
            f"{CONSTS.ROOT_DIR}/{self.instance.config_dictionary['default_address']}",
        )

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return CSVConfig().instance.dictionary

    # --
    # ...
    # --

    def operation(
        self, mode="", address="", file_name="", data: list = None, columns: list = None
    ) -> dict:  # type: ignore

        try:
            if mode == "":
                mode = self.mode

            if address == "":
                address = self.address

                if file_name:
                    address = address.replace(address[address.rfind("/") :], file_name)

            if mode == "w":
                data_frame = pandas.DataFrame(data, columns=columns)

                data_frame.to_csv(path_or_buf=address, index=False, encoding="utf-8-sig")

                return data_frame

            elif mode == "r":
                data_frame = pandas.read_csv(address).to_dict()
                return data_frame

        except Exception as exp:
            print(repr(exp))
            return False
