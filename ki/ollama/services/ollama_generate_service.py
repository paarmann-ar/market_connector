from ollama import chat
from ollama import generate
from ki.core.base import Base
from ki.ollama.config.ollama_config import OllamaConfig
from toolboxs.date_and_time import DateAndTime
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
        self.top_p = self.config_dictionary.get("top_p")

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
            self.prompt_on_screen(f"generate_with_ollama: ollamat start it on: {DateAndTime.get_now()}")

            response = generate(
                model=self.model,
                prompt=prompt,
                format="json",
                think=False,
                stream=False,
                options={
                    "num_predict": self.num_predict,
                    "temperature": self.temperature,
                    "num_ctx": self.num_ctx,
                    "top_p": float(self.top_p),
                },
                keep_alive="30m",
            )

            self.prompt_on_screen(f"generate_with_ollama: {bool(response)}")

            self.prompt_on_screen(f"generate_with_ollama: ollamat finished it on: {DateAndTime.get_now()}")

            return response

        except Exception as exp:
            print(f"generate_with_ollama: {exp}")
