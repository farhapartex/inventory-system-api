from django.http import HttpRequest
from django.utils import timezone
from django.db import transaction

from core.dtos import UserMinimalDTO
from core.enums import RoleEnum
from invoice.dtos import InvoiceCreateDTO, InvoiceCreateSuccessDTO, InvoiceItemMinimalDTO
from invoice.models import Invoice
from invoice.services.invoice_item_service import InvoiceItemService
from invoice.signals.signal import trigger_create_invoice_item_handler
from store.exceptions import ProductNotFoundException
from store.models import Employee
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
    def create_invoice(cls, *, request: HttpRequest, data: InvoiceCreateDTO) -> InvoiceCreateSuccessDTO:
        user = request.user
        store = None
        if user.role == RoleEnum.OWNER.name:
            store = user.store
        elif user.role == RoleEnum.SALES.name:
            employee = Employee.objects.filter(user=user).first()
            store = employee.store
        request_data = {
            "invoice_number": cls._get_unique_invoice_number(),
            "bill_to": data.bill_to,
            "date": data.date,
            "bill_from": data.bill_from,
            "store": store,
            "created_by": user
        }
        product_ids = [item.product_id for item in data.items]

        products = ProductService.get_products({"pk__in": product_ids, "is_active": True, "is_deleted": False})
        if products.count() != len(product_ids):
            raise ProductNotFoundException("Some products not found")

        with transaction.atomic():
            invoice = Invoice.objects.create(**request_data)

            trigger_create_invoice_item_handler.send(sender=invoice.__class__, request=request, invoice=invoice, items=data.items)
            items = InvoiceItemService.get_items(filter_data={"invoice_number": invoice.invoice_number, "invoice": invoice})

            invoice_item_dto = [InvoiceItemMinimalDTO(quantity=item.quantity, price=item.price, product=item.product.name) for item in items]
            created_by_dto = UserMinimalDTO(first_name=invoice.created_by.first_name, last_name=invoice.created_by.last_name, email=invoice.created_by.email)

            return InvoiceCreateSuccessDTO(
                bill_from=invoice.bill_from,
                bill_to=invoice.bill_to,
                date=invoice.date,
                amount=invoice.amount,
                is_paid=invoice.is_paid,
                paid_on=invoice.paid_on,
                items=invoice_item_dto,
                created_by=created_by_dto
            )

    @classmethod
    def retrieve_invoice(cls):
        pass

    @classmethod
    def invoice_list(cls):
        pass

    @classmethod
    def delete_invoice(cls):
        pass