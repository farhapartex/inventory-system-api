from django.contrib import admin
from core.models import User, UserAuthCode
# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "first_name", "last_name", "is_verified", 'is_staff', "is_superuser", "is_active")


@admin.register(UserAuthCode)
class UserAuthCodeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "code", "is_used")
