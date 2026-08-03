import re
import traceback
from typing import Any

from services.logging.config.log_config import LogConfig
from services.logging.core.base_log import BaseLog

# --
# ...
# --


class StackContext(BaseLog):
    object_name = None
    no_show_modules = None
    no_show_methods = None

    def __init__(self) -> None:
        StackContext.no_show_modules = self.get_config_dictionary().get(__name__).get(
            "no_show_modules")
        StackContext.no_show_methods = self.get_config_dictionary().get(__name__).get("no_show_methods")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return LogConfig().get_dictionary()

    # --
    # ...
    # --

    def __str__(cls) -> str:
        return cls.StackOperation()

    # --
    # ...
    # --
    @classmethod
    def StackOperation(cls, object_name="") -> Any:

        try:
            cls.object_name = object_name

            Stack: Any = ""

            if cls.object_name != "":
                Stack = re.search(r"([(]).+([)])", cls.object_name)

            else:
                for line in traceback.format_stack()[3:]:
                    # Data = re.search("([aq:]+\w+).+([, line ]+\d+).+([, in ]+\w+)", line)
                    Data = re.search(r"([aq:]+\w+).+([, line ]+\d+)", line)

                    if Data:
                        module = Data.group(1)[3:]
                        Line = Data.group(2)[1:]

                        if module not in cls.no_show_modules:
                            Data = re.search(r"(\b, in\b.\w+)", line)
                            method = "0"

                            if Data:
                                method = Data.group()[5:]

                                if method not in cls.no_show_methods:
                                    Stack = (
                                        Stack
                                        + " > "
                                        + module
                                        + "."
                                        + method
                                        + "("
                                        + Line
                                        + ")"
                                    )

            return Stack

        except Exception as exp:
            print(f"{__file__}--->{__name__} : + {exp!s}")
