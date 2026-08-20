from ollama import chat

from ki.core.base import Base
from ki.ollama.config.ollama_config import OllamaConfig

# --
# ...
# --


class OllamaChatService(Base):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.model = self.config_dictionary.get("model")

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

    def chat_with_ollama(self, message: list[dict]):

        try:
            response = chat(
                model=self.model,
                messages=message,
                format="json",
                options={"num_predict": 180, "temperature": 0.2, "num_ctx": 2048},
                keep_alive="30m",
            )

            self.prompt_on_screen(response)

            return response

        except Exception as exp:
            print(f"chat_with_ollama: {exp}")


# --
# ...
# --
