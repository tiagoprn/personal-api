# Factories can be used to auto-populate models for testing purposes.

import factory

from core.models import URLModel


class URLModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = URLModel
