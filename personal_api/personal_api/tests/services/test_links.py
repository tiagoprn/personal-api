import logging
import uuid

import pytest
import shortuuid

from core.services.links import (
    generate_shortened_hash,
    get_domain,
    sanitize_link,
    get_name_from_url,
)

logger = logging.getLogger(__name__)


def test_sanitize_link(real_urls):
    for record in real_urls:
        sanitized_link = sanitize_link(record['original'])
        expected_url = record['sanitized']
        logger.info(f'sanitized_link={sanitized_link}')
        assert sanitized_link == expected_url


def test_generate_shortened_hash():
    for _ in range(10):
        uid = uuid.uuid4()
        short_uuid = generate_shortened_hash(uid)
        assert shortuuid.decode(short_uuid) == uid


@pytest.mark.parametrize(
    'url,expected_domain',
    [
        ('http://www.example.test/foo/bar', 'www.example.test'),
        ('http://abc.hostname.com/somethings/anything/', 'abc.hostname.com'),
        ('https://tiagopr.nl/content/posts', 'tiagopr.nl'),
    ],
)
def test_get_domain(url, expected_domain):
    domain = get_domain(url)
    assert domain == expected_domain


@pytest.mark.parametrize(
    'url,expected_name',
    [
        (
            'https://flaviocopes.com/page/ebooks-links/',
            'flaviocopes.com ebooks-links',
        ),
        (
            'https://github.com/danth/pathfinder.vim',
            'github.com pathfinder.vim',
        ),
        (
            'https://fedoramagazine.org/how-to-use-poetry-to-manage-your-python-projects-on-fedora/',
            'fedoramagazine.org how-to-use-poetry-to-manage-your-python-projects-on-fedora',
        ),
        (
            'https://opensource.com/article/21/2/kubernetes-maintainer?utm_medium=Email&utm_campaign=weekly&sc_cid=7013a000002vqnQAAQ',
            'opensource.com kubernetes-maintainer',
        ),
        ('https://www.luos.io/', 'www.luos.io'),
        (
            'https://atthis.link/blog/2021/rss.html?utm_source=hackernewsletter&utm_medium=email&utm_term=fav',
            'atthis.link rss.html',
        ),
        ('http://me.io/', 'me.io'),
    ],
)
def test_get_name_from_url(url, expected_name):
    name = get_name_from_url(url)
    assert name == expected_name
