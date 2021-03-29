import logging
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from django_extensions.db.fields import AutoSlugField

from core.managers import LinkManager
from core.services.links import get_domain

logger = logging.getLogger(__name__)


class CustomUser(AbstractUser):
    def __str__(self):
        return self.username


class Link(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(unique=True, max_length=150, null=True, blank=True)
    slug = AutoSlugField(populate_from='name', overwrite=True)
    original_link = models.URLField(unique=True)
    sanitized_link = models.URLField(unique=True, null=True, blank=True)
    shortened_hash = models.CharField(
        unique=True, max_length=50, null=True, blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Customize the default manager to the one having the custom filters
    objects = LinkManager()

    def __str__(self):
        return str(self.slug)

    @property
    def domain(self):
        return get_domain(self.sanitized_link)
