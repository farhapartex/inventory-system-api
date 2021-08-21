from django.utils.translation import gettext_lazy as _
from django.db import models


class AccessLabelEnum(models.TextChoices):
    READ = "READ", _("Read")
    WRITE = "WRITE", _("Write")
    READ_WRITE = "READ_WRITE", _("Read and Write")
    NONE = "NONE", _("None")

    @classmethod
    def get_all(cls):
        return [cls.READ.value, cls.WRITE.value, cls.READ_WRITE.value, cls.NONE.value,]