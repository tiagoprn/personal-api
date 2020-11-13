from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        import core.signals  # pylint: disable=unused-import,import-outside-toplevel
