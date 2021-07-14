from django.apps import AppConfig


class ServicesConfig(AppConfig):
    name = 'services'

    def ready(self):
        from .import signals
