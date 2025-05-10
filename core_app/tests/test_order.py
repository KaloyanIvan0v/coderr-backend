from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from core_app.models import Order, UserProfile, OrderFeatures
from .test_data.order_data import LOGO_DESIGN_ORDER_DATA


class OrderViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            type='customer'
        )
        self.business_user = User.objects.create_user(
            username="businessuser",
            email="business@example.com",
            password="password123"
        )
        self.business_profile = UserProfile.objects.create(
            user=self.business_user,
            type='business'
        )

        order_data = LOGO_DESIGN_ORDER_DATA.copy()
        features = order_data.pop('features', [])

        self.order = Order.objects.create(
            customer_user=self.profile,
            business_user=self.business_profile,
            **order_data)

        for feature in features:
            OrderFeatures.objects.create(
                order=self.order,
                feature=feature)

    def test_create_order(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('order-list')
        response = self.client.post(url, LOGO_DESIGN_ORDER_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Order.objects.count(), 1)
        # self.assertEqual(Order.objects.get().title, "Logo Design")
