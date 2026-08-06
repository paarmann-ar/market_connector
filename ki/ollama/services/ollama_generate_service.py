from ollama import chat
from ollama import generate
from ki.core.base import Base
from ki.ollama.config.ollama_config import OllamaConfig

# --
# ...
# --


class OllamaGenerateService(Base):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.model = self.config_dictionary.get("model")
        self.num_predict = self.config_dictionary.get("num_predict")
        self.temperature = self.config_dictionary.get("temperature")
        self.num_ctx = self.config_dictionary.get("num_ctx")

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(cls):
        return OllamaConfig().get_dictionary()

    # --
    # ...
    # --

    def __call__(self) -> str:
        pass

    # --
    # ...
    # --

    def generate_with_ollama(self, prompt: str):

        try:
            response = generate(
                model=self.model,
                prompt=prompt,
                format="json",
                options={
                    "num_predict": self.num_predict,
                    "temperature": self.temperature,
                    "num_ctx": self.num_ctx,
                },
                keep_alive="30m",
            )

            self.prompt_on_screen(f"generate_with_ollama: {bool(response)}")

            return response

        except Exception as exp:
            print(f"generate_with_ollama: {exp}")
