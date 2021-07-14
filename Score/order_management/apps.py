from django.apps import AppConfig


class OrderManagementConfig(AppConfig):
    name = 'order_management'

    def ready(self):
        import order_management.signals