import json
from pathlib import Path
import CONSTS


class Cache:
    def __init__(self):
        self.cache_address = CONSTS.CACHE

    def get_from_cache(self, key: str, cache_file: str = "ollamat_cache.json") -> dict:
        ollamat_cache = Path(f"{self.cache_address}/{cache_file}")

        if not ollamat_cache.exists():
            return None

        try:
            with ollamat_cache.open("r", encoding="utf-8") as f:
                cache = json.load(f)

            return cache.get(key, None)

        except (json.JSONDecodeError, OSError):
            return None

    def update_cache(self, key: str, data: dict, cache_file: str = "ollamat_cache.json") -> dict:
        ollamat_cache = Path(f"{self.cache_address}/{cache_file}")
        ollamat_cache = Path(ollamat_cache)

        cache = {}

        if ollamat_cache.exists():
            try:
                with ollamat_cache.open("r", encoding="utf-8") as f:
                    cache = json.load(f)
            except (json.JSONDecodeError, OSError):
                cache = {}

        cache[key] = data

        with ollamat_cache.open("w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
