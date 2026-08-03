import CONSTS
from services.disk.json.json_manager import JSONManager

# --
# ...
# --


class FTPConfig:
    @classmethod
    def get_dictionary(cls, *args) -> dict:
        json = JSONManager()
        config_json = json.operation(CONSTS.CONFIG_JSON)

        return config_json[__name__] if __name__ in config_json else {}
