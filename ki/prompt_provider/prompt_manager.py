import CONSTS
from services.disk.file.file_manager import FileManager
from pathlib import Path

# --
# ...
# --


class PromptManager:
    # --
    # ...
    # --

    def __init__(self):
        pass

    # --
    # ...
    # --

    # "seo",
    # title=product.title,
    # description=product.description,

    def load_prompt_from_file(self, prompt_file_name: str, kwargs: dict) -> str:
        try:
            prompt = Path(f"{CONSTS.KI_PROMPT_DIR}{prompt_file_name}.md").read_text(encoding="utf-8")
            prompt = prompt.format(**kwargs)

            return prompt

        except Exception as exp:
            print(f"load_prompt_from_file: {exp}")
