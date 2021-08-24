from invoice.models import InvoiceItem


class InvoiceItemService:
    @classmethod
    def _get_items(cls, *, filter_data: dict):
        return InvoiceItem.get_filter_data(filter_data)

    @classmethod
    def get_items(cls, *, filter_data: dict):
        return cls._get_items(filter_data=filter_data)

    @classmethod
    def create_invoice_item(cls):
        pass

