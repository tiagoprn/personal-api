import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from core.models import Url
from core.services.urls import generate_shortened_hash, sanitize_url

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Url)
def trigger_generate_shortened_hash(
    sender, instance, created, **kwargs
):  # pylint: disable=unused-argument
    operation = 'CREATED' if created else 'UPDATED'
    logger.info(f'{operation}: Url slug="{instance.slug}"')
    instance.sanitized_url = sanitize_url(instance.original_url)
    instance.shortened_hash = generate_shortened_hash(uid=instance.uuid)
    instance.save()
