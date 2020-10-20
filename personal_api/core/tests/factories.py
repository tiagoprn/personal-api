# Factories can be used to auto-populate models for testing purposes.

import factory

from core.models import CustomUser, Url


class UserModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser


class UrlModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Url
