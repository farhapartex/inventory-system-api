import logging
from typing import List

from django.dispatch import receiver
from django.http import HttpRequest

from invoice.dtos import InvoiceItemCreateDTO
from invoice.models import InvoiceItem, Invoice
from invoice.signals.signal import trigger_create_invoice_item_handler
from store.services import ProductService

logger = logging.getLogger(__name__)


@receiver(trigger_create_invoice_item_handler, sender=Invoice)
def create_invoice_items(request: HttpRequest, invoice: Invoice, items: List[InvoiceItemCreateDTO], **kwargs):
    total_price = 0
    logger.critical("Invoice item creation started")
    for item in items:
        product = ProductService.get_products({"id": item.product_id, "is_active": True, "is_deleted": False}).first()
        data = {
            "invoice": invoice,
            "invoice_number": invoice.invoice_number,
            "product": product,
            "quantity": item.quantity,
            "price": product.selling_price
        }
        val = product.selling_price * item.quantity
        total_price += val

        InvoiceItem.objects.create(**data)

    logger.critical("Invoice item creation ended")
    invoice.amount = total_price
    invoice.save()

    logger.critical("Invoice info updated")

