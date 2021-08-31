from django.test import TestCase
from django.db.utils import IntegrityError
from django.db.utils import DataError
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


class UserAuthCodeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.UserFactory = UserAuthCodeFactory._meta.model

    def test_valid_user_auth_code_factory(self):
        user_auth_code = UserAuthCodeFactory.create()

        user_auth_codes = self.UserFactory.objects.all()
        self.assertEqual(user_auth_codes.count(), 1)
        self.assertEqual(user_auth_codes.first().user.username, user_auth_code.user.username)
        self.assertEqual(user_auth_code.is_used, False)
        self.assertTrue(len(user_auth_code.code) <= 6)

    def test_invalid_user_auth_code_factory(self):
        with self.assertRaises(DataError):
            UserAuthCodeFactory.create(code=fake.pystr())