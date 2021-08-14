from django.utils.translation import gettext_lazy as _
from django.db import models


class RoleEnum(models.TextChoices):
    ADMIN = "ADMIN", _("Admin")
    EDITOR = "EDITOR", _("Editor")
    SALES = "SALES", _("Sales")
    CUSTOMER = "CUSTOMER", _("Customer")
    OWNER = "OWNER", _("Owner")

    @classmethod
    def get_all(cls):
        return [cls.ADMIN.value, cls.EDITOR.value, cls.SALES.value, cls.CUSTOMER.value, cls.OWNER.value]