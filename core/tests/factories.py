import os
import factory
from faker import Faker
from faker.providers import lorem, person, python

from core.models import User

fake = Faker()
fake.add_provider(lorem)
fake.add_provider(person)
fake.add_provider(python)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User