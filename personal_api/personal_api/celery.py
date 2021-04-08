import os

from celery import Celery

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_api.settings')
app = Celery('personal_api')

# Celery will apply all configuration keys with defined namespace
app.config_from_object('django.conf:settings', namespace='CELERY')
# Load tasks from all registered apps
app.autodiscover_tasks()

app.conf.task_serializer = 'json'

app.conf.result_serializer = 'json'

app.conf.accept_content = ['json']

app.conf.task_create_missing_queues = True
