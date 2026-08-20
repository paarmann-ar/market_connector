import json
from pathlib import Path
import CONSTS

# --
# ...
# --


class Cache:
    def __init__(self):
        self.cache_address = CONSTS.CACHE

    # --
    # ...
    # --

    def get_from_cache(self, cache_file: str, is_change_k_v: bool = False, key: str = None) -> dict:
        cache_file = Path(f"{self.cache_address}/{cache_file}")

        if not cache_file.exists():
            return None

        try:
            with cache_file.open("r", encoding="utf-8") as f:
                cache = json.load(f)

            if is_change_k_v:
                return {value: key for key, value in cache.items()}

            return cache.get(key, None)

        except (json.JSONDecodeError, OSError):
            return None

    # --
    # ...
    # --

    def update_cache(self, key: str, data: dict, cache_file: str) -> dict:
        cache_file = Path(f"{self.cache_address}/{cache_file}")
        cache_file = Path(cache_file)

        cache = {}

        if cache_file.exists():
            try:
                with cache_file.open("r", encoding="utf-8") as f:
                    cache = json.load(f)
            except (json.JSONDecodeError, OSError):
                cache = {}

        cache[key] = data

        with cache_file.open("w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)


