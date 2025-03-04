from django.apps import AppConfig


class OrdersappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ordersapp"

    def ready(self):
        import ordersapp.signals  # Подключаем файл signals.py
