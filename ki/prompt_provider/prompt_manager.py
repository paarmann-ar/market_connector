from pathlib import Path
from string import Template

import CONSTS

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

    def load_prompt_from_file(self, prompt_file_name: str, kwargs: dict) -> str:
        try:
            prompt = Path(f"{CONSTS.KI_PROMPT_DIR}/{prompt_file_name}.md").read_text(encoding="utf-8")
            prompt = Template(prompt).safe_substitute(kwargs)

            return prompt

        except Exception as exp:
            print(f"load_prompt_from_file: {exp}")
