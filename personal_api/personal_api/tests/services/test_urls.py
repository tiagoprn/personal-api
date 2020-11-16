import uuid

import shortuuid

from core.services.urls import (
    generate_shortened_hash,
    get_domain,
    sanitize_url,
)


def test_sanitize_url():
    # TODO: implement
    pass


def test_generate_shortened_hash():
    for _ in range(10):
        uid = uuid.uuid4()
        short_uuid = generate_shortened_hash(uid)
        assert shortuuid.decode(short_uuid) == uid


def test_get_domain():
    # TODO: implement
    pass
