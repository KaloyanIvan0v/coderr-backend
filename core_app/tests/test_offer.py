from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from core_app.models import UserProfile, Offer


class OfferViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            type='customer'
        )

    def test_create_offer(self):
        url = reverse('offers-list')
        data = {
            'title': 'Test Offer',
            'description': 'Test Description',
            'price': 100
        }
        response = self.client.post(url, data, format='json')
