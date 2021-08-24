from django.http import HttpRequest
from django.utils import timezone
from invoice.dtos import InvoiceCreateDTO
from invoice.models import Invoice
from invoice.signals.signal import trigger_create_invoice_item_handler
from store.exceptions import ProductNotFoundException
from store.services import ProductService


class InvoiceService:
    @classmethod
    def _get_unique_invoice_number(cls) -> str:
        today = timezone.now()
        today_str = f"{today.year}{today.month}{today.day}"
        next_invoice_number = '01'
        last_invoice = Invoice.objects.filter(invoice_number__startswith=today_str).order_by('invoice_number').last()
        if last_invoice:
            last_invoice_number = int(last_invoice.invoice_number[6:])
            next_invoice_number = '{0:02d}'.format(last_invoice_number + 1)

        return f"{today_str}{next_invoice_number}"

    @classmethod
    def create_invoice(cls, *, request: HttpRequest, data: InvoiceCreateDTO):
        user = request.user
        request_data = {
            "invoice_number": cls._get_unique_invoice_number(),
            "bill_to": data.bill_to,
            "date": data.date,
            "bill_from": data.bill_from,
            "created_by": user
        }
        product_ids = [item.product_id for item in data.items]

        products = ProductService.get_products({"pk__in": product_ids, "is_active": True, "is_deleted": False})
        if products.count() != len(product_ids):
            raise ProductNotFoundException("Some products not found")

        invoice = Invoice.objects.create(**request_data)

        trigger_create_invoice_item_handler.send(sender=invoice.__class__, request=request, invoice=invoice, items=data.items)

    @classmethod
    def retrieve_invoice(cls):
        pass

    @classmethod
    def invoice_list(cls):
        pass

    @classmethod
    def delete_invoice(cls):
        pass