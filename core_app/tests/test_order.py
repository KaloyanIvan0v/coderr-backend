from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from core_app.models import Order, UserProfile, OrderFeatures, Offer, OfferDetails, OfferFeatures
from .test_helper.order_test_helper import ORDER_DATA, create_order
from .test_helper.offer_test_helper import OFFER_DATA, create_offer, create_offer_detail
from .test_helper.user_test_helper import create_user, create_user_profile


class OrderViewTests(APITestCase):
    def setUp(self):
        self.user = create_user("tomas_customer")
        self.profile = create_user_profile(self.user, "customer")

        self.business_user = create_user("markus_business")
        self.business_profile = create_user_profile(
            self.business_user, "business")

        self.offer = create_offer(self)
        self.offer_detail = create_offer_detail(self.offer)

        self.order = create_order(self, self.profile, self.business_profile)

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
        data = {"offer_detail_id": 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(response.data['status'], "in_progress")
        self.assertIn("Logo Design", response.data['features'])

    def test_create_order_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('orders-list')
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 1)

    def test_create_order_unauthorized(self):
        url = reverse('orders-list')
        data = ORDER_DATA.copy()
        data['customer_user'] = self.profile.id
        data['business_user'] = self.business_profile.id
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_order_forbidden(self):
        self.client.force_authenticate(user=self.business_user)
        url = reverse('orders-list')
        data = {"offer_detail_id": 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_order_not_found(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('orders-list')
        data = {"offer_detail_id": 999}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

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
        self.assertEqual(Order.objects.all()[0].status, "completed")

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
