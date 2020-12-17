# Factories can be used to auto-populate models for testing purposes.

import factory

from core.models import CustomUser, Link


class UserModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser


class LinkModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Link
