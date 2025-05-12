from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from core_app.models import UserProfile


class AuthViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='exampleUsername',
            email='example@mail.de',
            password='examplePassword'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            type='customer'
        )

    def test_register_user(self):
        url = reverse('registration')
        data = {
            "username": "exampleUsername2",
            "email": "example2@mail.de",
            "password": "examplePassword2",
            "repeated_password": "examplePassword2",
            "type": "customer"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.data)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        self.assertIn('user_id', response.data)

    def test_invalid_login_user(self):
        url = reverse('login')
        data = {
            "username": "exampleUsername8"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user(self):

        url = reverse('login')
        data = {
            "username": "exampleUsername",
            "password": "examplePassword"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        self.assertIn('user_id', response.data)
