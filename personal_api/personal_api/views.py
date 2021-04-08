import logging
import os
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from random import randint

import django
from django.conf import settings
from django.db.migrations.recorder import MigrationRecorder

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from core.tasks import check_celery_is_up

logger = logging.getLogger(__name__)


@lru_cache(maxsize=None)
def get_app_version():
    root_path = str(Path().absolute())
    with open(os.path.join(root_path, 'VERSION'), 'r') as version_file:
        return version_file.read().replace('\n', '')


@lru_cache(maxsize=None)
def get_last_migration():
    try:
        last_migration = MigrationRecorder.Migration.objects.filter(
            app='core'
        ).last()
        return last_migration.name

    except AttributeError:
        logging.info(
            'It seems the core app does not '
            'have models and therefore migrations, '
            'so trying the django default auth app instead.'
        )
        last_migration = MigrationRecorder.Migration.objects.filter(
            app='auth'
        ).last()
        return f'{last_migration.name} (django auth app)'


class HealthcheckLiveness(APIView):
    """
    The kubelet uses liveness probes to know when to restart a Container. For
    example, liveness probes could catch a deadlock, where an application is
    running, but unable to make progress. Restarting a Container in such a
    state can help to make the application more available despite bugs. This
    will run ON REGULAR INTERVALS.
    """

    permission_classes = ()

    def get_worker_liveness(self):
        live = 'NO'
        broker = '?'
        timestamp = datetime.now().isoformat()
        timezone = '?'
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        try:
            timezone = settings.TIME_ZONE

            random_number = randint(1000, 9999)
            now_timestamp = datetime.now().isoformat()

            # The function below is actually a celery task,
            # that must have a celery worker up listening to
            # the queue testing_queue so that it can be executed.
            # See this project Makefile runworker command to see
            # how it is started.
            check_celery_is_up.apply_async(
                kwargs={
                    'random_number': random_number,
                    'now_timestamp': now_timestamp,
                }
            )
            live = 'OK'
            status_code = status.HTTP_200_OK
            broker = settings.CELERY_BROKER_BACKEND
            if broker == 'rabbitmq':
                host_port = settings.CELERY_BROKER_URL.split('@')[1]
                broker += f' ({host_port})'

        except Exception as ex:
            logging.exception(f'Liveness Healthcheck failed. Exception: {ex}')

        response_dict = {
            'live': live,
            'broker': broker,
            'name': 'personal-api',
            'version': get_app_version(),
            'timestamp': timestamp,
            'timezone': timezone,
        }
        logger.debug(response_dict)

        return Response(response_dict, status_code)

    def get_api_liveness(self):
        live = 'NO'
        migration_name = '?'
        timestamp = datetime.now().isoformat()
        timezone = '?'
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        try:
            timezone = settings.TIME_ZONE
            migration_name = get_last_migration()
            live = 'OK'
            status_code = status.HTTP_200_OK
        except Exception as ex:
            logging.exception(f'Liveness Healthcheck failed. Exception: {ex}')

        response_dict = {
            'live': live,
            'name': 'personal-api',
            'version': get_app_version(),
            'last_migration': migration_name,
            'timestamp': timestamp,
            'timezone': timezone,
        }
        logger.debug(response_dict)

        return Response(response_dict, status_code)

    def get(self, _request):  # pylint: disable=no-self-use
        return self.get_api_liveness()


class HealthcheckReadiness(APIView):
    """
    The kubelet uses readiness probes to know when a Container is ready to
    start accepting traffic. A Pod is considered ready when all of its
    Containers are ready. One use of this signal is to control which Pods are
    used as backends for Services. When a Pod is not ready, it is removed from
    Service load balancers. This will run ONLY ONCE.
    """

    permission_classes = ()

    def get(self, _request):  # pylint: disable=no-self-use
        app_type = 'django-framework'
        app_type += f' {django.get_version()}'
        response_dict = {
            'ready': 'OK',
            'app_name': 'personal-api',
            'app_version': get_app_version(),
            'app_type': app_type,
        }
        logger.debug(response_dict)
        return Response(response_dict, status.HTTP_200_OK)
