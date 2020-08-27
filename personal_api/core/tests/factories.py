# Factories can be used to auto-populate models for testing purposes.

import factory

from core.models import SampleModel


class SampleModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SampleModel
