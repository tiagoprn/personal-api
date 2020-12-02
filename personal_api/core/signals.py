import logging

from django.db.models.signals import post_save

from core.models import Url
from core.services.urls import generate_shortened_hash, sanitize_url

logger = logging.getLogger(__name__)


def _save_avoiding_infinite_post_save_signal_loop(instance):
    post_save.disconnect(
        trigger_generate_shortened_hash,
        sender=Url,
        dispatch_uid='trigger_generate_shortened_hash',
    )

    instance.save()

    post_save.connect(
        trigger_generate_shortened_hash,
        sender=Url,
        dispatch_uid='trigger_generate_shortened_hash',
    )


def trigger_generate_shortened_hash(
    sender, instance, created, **kwargs
):  # pylint: disable=unused-argument
    operation = 'CREATED' if created else 'UPDATED'
    logger.info(f'{operation}: Url slug="{instance.slug}"')
    instance.sanitized_url = sanitize_url(instance.original_url)
    instance.shortened_hash = generate_shortened_hash(uid=instance.id)
    _save_avoiding_infinite_post_save_signal_loop(instance)


post_save.connect(
    trigger_generate_shortened_hash,
    sender=Url,
    dispatch_uid='trigger_generate_shortened_hash',
)
