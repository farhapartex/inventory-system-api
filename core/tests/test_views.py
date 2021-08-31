from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from core.tests.factories import *
from core.models import User
from core.tests.factories import *


class UserRegistrationTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.url = reverse('user-registration')

    def test_url_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_with_valid_data(self):
        email = fake.unique.email()
        data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": email,
            "password": fake.pystr()
        }

        response = self.client.post(self.url, data, format="json")
        res_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(email=email)
        self.assertEqual(user.username, email)
        self.assertEqual(user.username, res_data["user"]["username"])

    def test_with_invalid_data(self):
        data = {}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name()
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_with_existing_user(self):
        email = fake.email()
        UserFactory.create(username=email, email=email, is_active=True)

        data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": email,
            "password": fake.pystr()
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)


class UserAuthCodeTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse("user-account-verify")
        cls.registration_url = reverse('user-registration')

    def test_with_valid_user(self):
        email = fake.unique.email()
        data = {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": email,
            "password": fake.pystr()
        }

        response = self.client.post(self.registration_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        auth_code = UserAuthCode.objects.filter(user__email=email, is_used=False).first()

        data = {
            "email": email,
            "code": auth_code.code
        }

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = User.get_instance({"email": email})
        self.assertEqual(user.is_verified, True)
        self.assertEqual(user.is_active, True)
