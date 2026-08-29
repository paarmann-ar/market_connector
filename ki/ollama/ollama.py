import json

from ki.core.base import Base
from ki.ollama.config.ollama_config import OllamaConfig
from ki.ollama.models.ollama_message_model import OllamaMessageModel
from ki.ollama.models.ollama_prompt_model import OllamaPromptModel
from ki.ollama.services.ollama_chat_service import OllamaChatService
from ki.ollama.services.ollama_generate_service import OllamaGenerateService
from ki.models.input_message_model import InputMessageModel
from ki.ollama.models.ollama_answer_model import ProductOutputModel

# --
# ...
# --


class Ollama(Base):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.cache_file_name = self.config_dictionary.get("cache_file_name")

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
    ) -> ProductOutputModel:

        try:
            cache = self.cache.get_from_cache(cache_file=self.cache_file_name, key=input_message_model.inputs.get("cache_id"))
            if cache:
                return ProductOutputModel(**cache)

            if not ollama_prompt_model:
                ollama_prompt_model = self.convert_prompt_model_to_ollama_prompt_model(input_message_model)

            error_product_dict = input_message_model.to_dict()

            default_return = {
                "title": f"kapput!{error_product_dict.get('title', '')}",
                "description": error_product_dict.get("description", ""),
                "short_description": error_product_dict.get("short_description", ""),
                "meta_description": error_product_dict.get("short_description", ""),
                "focus_keywords": [error_product_dict.get("brand", ""), ""],
                "primary_focus_keyword": error_product_dict.get("brand", "No-Brand"),
                "slug": error_product_dict.get("slug", "No-Slug"),
            }

            response = self.ollama_generate_service.generate_with_ollama(prompt=ollama_prompt_model.content)
            response = response.get("response", "").strip()
            response = ProductOutputModel.model_validate_json(response)

            response = response.model_dump()
            self.cache.update_cache(key=input_message_model.inputs.get("cache_id"), data=response, cache_file=self.cache_file_name)

            return ProductOutputModel(**response)

        except json.JSONDecodeError as exp:
            self.error("Invalid JSON from Ollama: %s | Response: %s", exp)
            return default_return

        except Exception as exp:
            self.error(f"get_seo_from_ollama_generate_for_rankmath: {exp}")
