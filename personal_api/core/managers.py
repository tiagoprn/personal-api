from datetime import datetime, timedelta

from django.db import models


class UrlManager(models.Manager):
    def from_user(self, user):
        queryset = self.get_queryset()
        return queryset.filter(user=user)

    def recently_updated(self, days, user=None):
        queryset = self.from_user(user=user) if user else self.get_queryset()

        now_timestamp = datetime.now()
        days_ago_timestamp = now_timestamp - timedelta(days=days)

        return queryset.filter(
            models.Q(updated_at__gte=days_ago_timestamp)
            & models.Q(updated_at__lte=now_timestamp)
        )
