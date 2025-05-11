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
        url = reverse('orders-list')

        data = LOGO_DESIGN_ORDER_DATA.copy()
        data['customer_user'] = self.profile.id
        data['business_user'] = self.business_profile.id

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Order.objects.last().title, "Logo Design")

    def test_update_order(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('orders-detail', kwargs={'pk': self.order.id})

    def test_delete_order(self):
        pass

    def test_order_count(self):
        pass

    def test_completed_order_count(self):
        pass
