from django.contrib import admin
from invoice.models import Invoice, InvoiceItem
# Register your models here.


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "store", "invoice_number", "date", "amount", "is_paid", "paid_on")


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ("id", "invoice_number", "product", "quantity", "price")

