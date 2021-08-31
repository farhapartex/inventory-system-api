from django.test import TestCase
from django.db.utils import IntegrityError
from core.tests.factories import UserFactory
from core.tests.factories import *


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.User = UserFactory._meta.model

    def test_valid_user_factory(self):
        user = UserFactory.create()

        users = self.User.objects.all()
        self.assertEqual(users.count(), 1)
        self.assertEqual(users.first().username, user.username)
        self.assertEqual(user.username, user.email)

    def test_unique_username(self):
        username = fake.email()
        user = UserFactory.create(username=username, email=username)
        self.assertEqual(user.email, username)

        with self.assertRaises(IntegrityError):
            UserFactory.create(username=username, email=username)
