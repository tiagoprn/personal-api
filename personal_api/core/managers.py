from datetime import datetime, timedelta

from django.db import models


class UrlQuerySet(models.QuerySet):
    # The queryset is useful so that we can combine this filter
    # with others from the ORM, so that it can be as flexible
    # as possible.
    def most_recent(self, days):
        timestamp = datetime.now() - timedelta(days=days)
        return self.filter(updated_at__gt=timestamp)

    def from_user(self, user):
        return self.filter(user=user)


class UrlManager(models.Manager):
    def get_queryset(self):
        return UrlQuerySet(self.model, using=self._db)

    def most_recent(self, days):
        return self.get_queryset().most_recent(days)

    def from_user(self, user):
        return self.get_queryset().from_user(user)
