import uuid

from django.db import models
from django_extensions.db.fields import AutoSlugField

from core.services.urls import clean_url


class URLModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(unique=True, max_length=150)
    slug = AutoSlugField(populate_from='name', overwrite=True)
    original_url = models.URLField(unique=True)
    shortened_url = models.URLField(unique=True)

    # TODO: add user fk here, and a manager to only
    #       get model instances from the same user

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.slug)

    @property
    def cleaned_url(self) -> str:
        return clean_url(self.url)

    # TODO: on save, call services.urls.shorten_url
