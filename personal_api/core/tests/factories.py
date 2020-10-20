# Factories can be used to auto-populate models for testing purposes.

import factory

from core.models import CustomUser, URLModel


class UserModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser


class URLModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = URLModel
