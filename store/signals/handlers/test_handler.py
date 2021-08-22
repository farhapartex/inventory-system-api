import logging
from django.dispatch import receiver

from core.models import User
from store.signals import trigger_test_signal
from store.models import Store


logger = logging.getLogger(__name__)


@receiver(trigger_test_signal, sender=User)
def test_handler(owner, **kwargs):
    print("Working from print")
    logger.critical("Working from critical")
    logger.info("Working from critical")
    logger.error("Working from critical")
    Store.objects.create(owner=owner, name="Test ka baccha")

