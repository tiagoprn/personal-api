import uuid

from django.db import models
from django_extensions.db.fields import AutoSlugField


class SampleModel(models.Model):
    """
    The model below illustrated some of our model best practices, like:

    - UUID fields as ID
    - How to use slug fields
    - How to deal with a field that has predefined values.

    Since this model is only for guidance, it must be removed as soon as
    possible .  No migration was created with this model.
    """

    COMPLEXITY_CHOICES = (('s', 'Simple'), ('c', 'Complex'))

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    name = models.CharField(unique=True, max_length=150)

    slug = AutoSlugField(populate_from='name', overwrite=True)

    complexity = models.CharField(
        choices=COMPLEXITY_CHOICES, default='s', max_length=1
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.slug)
