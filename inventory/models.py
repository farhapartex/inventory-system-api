from django.db import models


class BaseAbstractEntity(models.Model):
    class Meta:
        abstract = True


class BaseEntity(BaseAbstractEntity):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    @classmethod
    def get_instance(cls, filter_dict: dict):
        instance = cls.objects.filter(**filter_dict).first()
        return instance

    @classmethod
    def get_filter_data(cls, filter_dict: dict):
        queryset = cls.objects.filter(**filter_dict)
        return queryset

    @classmethod
    def delete_instance(cls, pk: int):
        instance = cls.get_instance({"id": pk})
        instance.is_active = False
        instance.is_deleted = True
        instance.save()

    class Meta:
        abstract = True
