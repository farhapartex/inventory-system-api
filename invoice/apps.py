from django.apps import AppConfig


class InvoiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'invoice'

    def ready(self):
        import invoice.signals.handlers
