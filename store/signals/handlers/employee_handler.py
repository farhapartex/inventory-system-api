import logging
from django.dispatch import receiver
from django.http import HttpRequest

from core.models import User
from store.models import Employee, Store
from store.signals import trigger_create_employee

logger = logging.getLogger(__name__)


@receiver(trigger_create_employee, sender=User)
def create_store_employee_handler(request: HttpRequest, employee: User, store: Store, **kwargs):
    logger.critical("Employee is creating")
    Employee.objects.create(user=employee, store=store)
    logger.critical("Employee created!")

