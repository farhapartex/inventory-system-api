from django.db import models
from django.utils.translation import gettext_lazy as _
from inventory.models import BaseEntity
from core.models import User
# Create your models here.


class Store(BaseEntity):
    owner = models.OneToOneField(User, related_name="store", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Employee(BaseEntity):
    store = models.ForeignKey(Store, related_name="employees", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="+", on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.store.name}"


class ProductCategory(BaseEntity):
    store = models.ForeignKey(Store, related_name="categories", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(BaseEntity):
    store = models.ForeignKey(Store, related_name="products", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(ProductCategory, related_name="products", on_delete=models.DO_NOTHING)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    stock_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.name

