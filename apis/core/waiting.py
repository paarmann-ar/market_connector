from toolboxs.decorators import singleton
from toolboxs.delay import Delay

# --
# ...
# --


@singleton
class Wating:
    @classmethod
    def __call__(cls, delay=1000, message="") -> str:
        if message:
            print(message)

        Delay(delay)
