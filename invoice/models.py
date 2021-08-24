from django.db import models

from core.models import User
from inventory.models import BaseEntity
# Create your models here.
from store.models import Product


class Invoice(BaseEntity):
    invoice_number = models.CharField(max_length=255)
    bill_from = models.TextField()
    bill_to = models.TextField()
    date = models.DateField()
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
    paid_on = models.DateField(null=True)
    created_by = models.ForeignKey(User, related_name="+", null=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.invoice_number


class InvoiceItem(BaseEntity):
    invoice = models.ForeignKey(Invoice, related_name="invoice_items", on_delete=models.DO_NOTHING)
    invoice_number = models.CharField(max_length=255)
    product = models.ForeignKey(Product, related_name="+", on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.invoice_number} - {self.product.name}"

