from ki.ollama.ollama import Ollama
from toolboxs.decorators import singleton

# --
# ...
# --


@singleton
class KiProvider:
    def __init__(self, **kwargs):
        self.ollama = Ollama()
