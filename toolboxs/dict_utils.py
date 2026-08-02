from dataclasses import asdict, is_dataclass

# --
# ...
# --


def remove_none(obj):
    if is_dataclass(obj):
        obj = asdict(obj)

    if isinstance(obj, dict):
        return {k: remove_none(v) for k, v in obj.items() if v is not None}

    if isinstance(obj, list):
        return [remove_none(item) for item in obj]

    return obj
