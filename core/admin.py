from django.contrib import admin
from core.models import User
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "is_verified", 'is_staff', "is_superuser", "is_active")
