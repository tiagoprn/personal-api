import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Url
from core.services.urls import shorten_url

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Url)
def trigger_clean_and_shorten_url(
    sender, instance, created, **kwargs
):  # pylint: disable=unused-argument
    operation = 'CREATED' if created else 'UPDATED'
    logger.info(f'{operation}: Url slug="{instance.slug}"')
    instance.shortened_url = shorten_url(
        url=instance.original_url, uuid=instance.uuid
    )
    instance.save()
