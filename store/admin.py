from django.contrib import admin
from store.models import Store, ProductCategory, Product
# Register your models here.


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass
