import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django_extensions.db.fields import AutoSlugField

from core.services.urls import clean_url


class CustomUser(AbstractUser):
    def __str__(self):
        return self.username


class Url(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(unique=True, max_length=150)
    slug = AutoSlugField(populate_from='name', overwrite=True)
    original_url = models.URLField(unique=True)
    shortened_url = models.URLField(unique=True, null=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.slug)

    @property
    def cleaned_url(self) -> str:
        return clean_url(self.url)
