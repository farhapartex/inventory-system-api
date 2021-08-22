import logging
from django.dispatch import receiver

from core.models import User
from store.models import Employee
from store.signals import trigger_create_employee

logger = logging.getLogger(__name__)


@receiver(trigger_create_employee, sender=User)
def create_store_employee_handler(user, store, **kwargs):
    logger.info("Employee is creating")
    #Employee.objects.create(user=user, store=store)
    logger.info("Employee created!")

