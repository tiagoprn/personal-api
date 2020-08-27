# Below is necessary so that the django app can get the broker credentials
# to properly send the tasks to it.

from personal_api.celery import app as celery_app

__all__ = ('celery_app',)
