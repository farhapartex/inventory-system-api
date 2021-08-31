import os
import factory
from faker import Faker
from faker.providers import lorem, person, python

from core.enums import RoleEnum
from core.models import User, UserAuthCode

fake = Faker()
fake.add_provider(lorem)
fake.add_provider(person)
fake.add_provider(python)

user_fake_email = fake.unique.email()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda _: user_fake_email)
    email = factory.LazyAttribute(lambda _: user_fake_email)
    is_staff = factory.LazyAttribute(lambda _: False)
    is_superuser = factory.LazyAttribute(lambda _: False)
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    role = factory.LazyAttribute(lambda _: RoleEnum.ADMIN.name)


class UserAuthCodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserAuthCode

    user = factory.SubFactory(UserFactory)
    code = factory.LazyAttribute(lambda _: str(fake.pyint()))

