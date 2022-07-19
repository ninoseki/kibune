from ulid import ULID


def get_ulid() -> str:
    return str(ULID())
