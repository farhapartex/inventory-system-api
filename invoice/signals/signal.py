from django.dispatch import Signal

trigger_create_invoice_item_handler = Signal(providing_args=["request", "invoice", "items"])
