from functools import lru_cache

import yaml


@lru_cache(maxsize=256)
def parse_yaml(string: str):
    return yaml.safe_load(string)


def is_yaml(string: str) -> bool:
    try:
        parse_yaml(string)
        return True
    except yaml.error.YAMLError:
        return False
