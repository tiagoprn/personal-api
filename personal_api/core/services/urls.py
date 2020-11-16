import uuid

import requests
import shortuuid


def sanitize_url(url: str) -> str:
    response = requests.get(url, allow_redirects=True)
    if response.status_code == 200:
        url = response.url
    else:
        raise Exception(
            f'Unexpected status code {response.status_code} '
            f'trying to reach url={url}.'
        )

    url, _ = url.split('?')
    return url


def generate_shortened_hash(uid: uuid.UUID) -> str:
    return shortuuid.encode(uid)


def get_domain(url: str) -> str:
    # TODO
    return url
