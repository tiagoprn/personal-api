import logging

from django.db.models.signals import post_save

from core.models import Link
from core.services.links import generate_shortened_hash, sanitize_link

logger = logging.getLogger(__name__)


def trigger_generate_shortened_hash(
    sender, instance, created, **kwargs
):  # pylint: disable=unused-argument
    operation = 'CREATED' if created else 'UPDATED'
    logger.info(f'{operation}: Link slug="{instance.slug}"')
    instance.sanitized_link = sanitize_link(instance.original_link)
    instance.shortened_hash = generate_shortened_hash(uid=instance.id)
    _save_avoiding_infinite_post_save_signal_loop(instance)


URL_POST_SAVE_PARAMS = {
    'receiver': trigger_generate_shortened_hash,
    'sender': Link,
    'dispatch_uid': 'trigger_generate_shortened_hash',
}


def _save_avoiding_infinite_post_save_signal_loop(instance):
    post_save.disconnect(**URL_POST_SAVE_PARAMS)
    instance.save()
    post_save.connect(**URL_POST_SAVE_PARAMS)


post_save.connect(**URL_POST_SAVE_PARAMS)
