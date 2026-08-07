from ki.core.base import Base
from ki.ollama.config.ollama_config import OllamaConfig
from ki.ollama.models.ollama_message_model import OllamaMessageModel
from ki.ollama.models.ollama_prompt_model import OllamaPromptModel
from ki.ollama.services.ollama_chat_service import OllamaChatService
from ki.ollama.services.ollama_generate_service import OllamaGenerateService

from ki.prompt_provider.models.input_message_model import InputMessageModel
import json

# --
# ...
# --


class Ollama(Base):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.ollama_chat_service = OllamaChatService()
        self.ollama_generate_service = OllamaGenerateService()

        self.prompt_on_screen(f"{__class__.__name__}, {id(self)}")

    # --
    # ...
    # --

    @classmethod
    def get_config_dictionary(self):
        return OllamaConfig().get_dictionary()

    # --
    # ...
    # --

    def convert_prompt_model_to_ollama_message_model(self, input_message: InputMessageModel) -> OllamaMessageModel:

        try:
            message = self.prompt_manager.load_prompt_from_file(input_message.md_file_name, input_message.inputs)

            # "seo",
            # title=product.title,
            # description=product.description,

            ollama_message_model = OllamaMessageModel()
            ollama_message_model.content = message

            return ollama_message_model

        except Exception as exp:
            self.error(f"convert_prompt_model_to_ollama_message_model: {exp}")

    # --
    # ...
    # --

    def convert_prompt_model_to_ollama_prompt_model(self, input_message: InputMessageModel) -> OllamaPromptModel:

        try:
            message = self.prompt_manager.load_prompt_from_file(input_message.md_file_name, input_message.inputs)

            # "seo",
            # title=product.title,
            # description=product.description,

            ollama_prompt_model = OllamaPromptModel()
            ollama_prompt_model.content = message

            return ollama_prompt_model

        except Exception as exp:
            self.error(f"convert_prompt_model_to_ollama_prompt_model: {exp}")

    # --
    # ...
    # --

    def get_seo_from_ollama_chat_for_rankmath(
        self,
        input_message_model: InputMessageModel = None,
        ollama_message_model: OllamaMessageModel = None,
    ) -> dict:

        try:
            if not ollama_message_model:
                ollama_message_model = self.convert_prompt_model_to_ollama_message_model(input_message_model)

            response = self.ollama_chat_service.chat_with_ollama([ollama_message_model.to_dict()])
            response = response["message"]["content"]

            response = json.loads(response)

            return response

        except Exception as exp:
            self.error(f"get_seo_from_ollama_chat_for_rankmath: {exp}")

    # --
    # ...
    # --

    def get_seo_from_ollama_generate_for_rankmath(
        self,
        input_message_model: InputMessageModel = None,
        ollama_prompt_model: OllamaPromptModel = None,
    ) -> dict:

        try:
            if not ollama_prompt_model:
                ollama_prompt_model = self.convert_prompt_model_to_ollama_prompt_model(input_message_model)

            response = self.ollama_generate_service.generate_with_ollama(prompt=ollama_prompt_model.content)
            response = response.get("response", "").strip()

            # print("========== OLLAMA RAW RESPONSE ==========")
            # print(response)
            # print("==========================================")

            response = json.loads(response)

            return response

        except json.JSONDecodeError as exp:
            self.error(
                "Invalid JSON from Ollama: %s | Response: %s",
                exp,
                response[:2000],
            )
            return {}

        except Exception as exp:
            self.error(f"get_seo_from_ollama_generate_for_rankmath: {exp}")
