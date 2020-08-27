# This is where you can put your celery tasks.

import logging

from celery import task

logger = logging.getLogger(__name__)


@task(  # pylint: disable=not-callable
    name='check_celery_is_up',
    queue='my-replicant-project-healthcheck',
    max_retries=3,
    default_retry_delay=60,
)
def check_celery_is_up(random_number: int, now_timestamp: str) -> None:
    """
    An example of a view calling this task can be seen at
    my_replicant_project.views.HealthcheckLiveness.get() .
    """
    logger.info(
        f'check_celery_is_up: generated random number '
        f'{random_number} at {now_timestamp}.'
    )
