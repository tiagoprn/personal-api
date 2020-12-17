import logging
import uuid
from urllib.parse import urlparse

import requests
import shortuuid

logger = logging.getLogger(__name__)


def sanitize_link(url: str) -> str:
    response = requests.get(url, allow_redirects=True)
    if response.status_code == 200:
        url = response.url
    else:
        raise Exception(
            f'Unexpected status code {response.status_code} '
            f'trying to reach url={url}.'
        )

    if '?' in url:
        url, _ = url.split('?')

    if url.endswith('/'):
        url = url[:-1]

    return url


def generate_shortened_hash(uid: uuid.UUID) -> str:
    return shortuuid.encode(uid)


def get_domain(url: str) -> str:
    parsed_url = urlparse(url)
    return parsed_url.netloc
