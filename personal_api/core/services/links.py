import logging
import re
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


def get_name_from_url(url: str) -> str:
    if url.endswith('/'):
        url = url[0:-1]

    domain = get_domain(url)

    scheme = urlparse(url).scheme

    protocol = f'{scheme}://'
    partial_uri = url.replace(protocol, '').replace(domain, '')

    uri = ''
    if '/' in partial_uri:
        uri = partial_uri.split('/')[-1]
        if '?' in uri:
            uri = uri.split('?')[0]

    name = f'{domain} {uri}'.strip()

    return name
