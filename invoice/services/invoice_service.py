from django.http import HttpRequest

from invoice.dtos import InvoiceCreateDTO


class InvoiceService:
    @classmethod
    def create_invoice(cls, *, request: HttpRequest, data: InvoiceCreateDTO):
        user = request.user

    @classmethod
    def retrieve_invoice(cls):
        pass

    @classmethod
    def invoice_list(cls):
        pass

    @classmethod
    def delete_invoice(cls):
        pass