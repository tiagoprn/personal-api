from datetime import datetime, timedelta

from django.db import models


class UrlQuerySet(models.QuerySet):
    # The queryset is useful so that we can combine this filter
    # with others from the ORM, so that it can be as flexible
    # as possible.
    def recently_updated(self, days):
        now_timestamp = datetime.now()
        days_ago_timestamp = now_timestamp - timedelta(days=days)

        return self.filter(
            models.Q(updated_at__gte=days_ago_timestamp)
            & models.Q(updated_at__lte=now_timestamp)
        )

    def from_user(self, user):
        return self.filter(user=user)


class UrlManager(models.Manager):
    def get_queryset(self):
        return UrlQuerySet(self.model, using=self._db)

    def recently_updated(self, days):
        return self.get_queryset().recently_updated(days)

    def from_user(self, user):
        return self.get_queryset().from_user(user)
