import uuid

import shortuuid


def clean_url(url: str) -> str:
    url, _ = url.split('?')
    return url


def generate_shortened_hash(uid: uuid.UUID) -> str:
    return shortuuid.encode(uid)
