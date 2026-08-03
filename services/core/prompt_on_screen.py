import colorama

import CONSTS
from toolboxs.decorators import singleton

# --
# ...
# --


@singleton
class PromptOnScreen:
    @classmethod
    def __call__(cls, message="") -> str:
        colorama.init()
        print(f"{CONSTS.COLORS.AQUA_PROMPT.value}{message}{CONSTS.COLORS.ENDC.value}")
