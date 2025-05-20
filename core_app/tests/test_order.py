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

    def test_get_order_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('orders-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.count(), 1)

    def test_get_order_list_unauthorized(self):
        url = reverse('orders-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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
        self.assertEqual(Order.objects.last().status, "in_progress")

    def test_create_order_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('orders-list')
        data = LOGO_DESIGN_ORDER_DATA.copy()
        data['customer_user'] = self.profile.id
        data['business_user'] = self.business_profile.id
        data['title'] = ''
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 1)

    def test_create_order_unauthorized(self):
        url = reverse('orders-list')
        data = LOGO_DESIGN_ORDER_DATA.copy()
        data['customer_user'] = self.profile.id
        data['business_user'] = self.business_profile.id
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_forbidden(self):
        self.client.force_authenticate(user=self.business_user)
        url = reverse('orders-list')
        data = LOGO_DESIGN_ORDER_DATA.copy()
        data['customer_user'] = self.profile.id
        data['business_user'] = self.business_profile.id
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_order_details_unauthorized(self):
        url = reverse('orders-detail', kwargs={'pk': self.order.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_order(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('orders-detail', kwargs={'pk': self.order.id})
        data = {
            "status": "completed"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.last().status, "completed")

    def test_non_superuser_cannot_delete_order(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('orders-detail', kwargs={'pk': self.order.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Order.objects.count(), 1)

    def test_superuser_can_delete_order(self):
        superuser = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )
        self.client.force_authenticate(user=superuser)
        url = reverse('orders-detail', kwargs={'pk': self.order.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Order.objects.count(), 0)

    def test_order_count(self):
        self.client.force_authenticate(user=self.user)
        url = reverse(
            'order-count', kwargs={'business_user_id': self.business_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_count'], 1)

    def test_completed_order_count(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('completed-order-count',
                      kwargs={'business_user_id': self.business_user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['order_count'], 0)
