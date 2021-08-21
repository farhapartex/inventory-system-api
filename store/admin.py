from django.contrib import admin
from store.models import Store, ProductCategory, Product, Employee
# Register your models here.


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "is_active", "is_deleted")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "store", "user")

    
@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "store", "is_active", "is_deleted")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
