import logging
import uuid

import shortuuid

from core.services.urls import (
    generate_shortened_hash,
    get_domain,
    sanitize_url,
)

logger = logging.getLogger(__name__)


def test_sanitize_url(real_urls):
    for record in real_urls:
        sanitized_url = sanitize_url(record['original'])
        expected_url = record['sanitized']
        logger.info(f'sanitized_url={sanitized_url}')
        assert sanitized_url == expected_url


def test_generate_shortened_hash():
    for _ in range(10):
        uid = uuid.uuid4()
        short_uuid = generate_shortened_hash(uid)
        assert shortuuid.decode(short_uuid) == uid


def test_get_domain():
    # TODO: implement
    pass
