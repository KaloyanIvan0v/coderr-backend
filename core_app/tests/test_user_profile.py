from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from core_app.models import UserProfile

from .test_data.user_data import UPDATE_USER_DATA


class ProfileViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )
        self.user_business = User.objects.create_user(
            username='testuser_business',
            email='test_business@example.com',
            password='password123'
        )
        self.user_business_2 = User.objects.create_user(
            username='testuser_business_2',
            email='test_business_2@example.com',
            password='password123'
        )

        self.profile = UserProfile.objects.create(
            user=self.user,
            type='customer'
        )
        self.profile_business = UserProfile.objects.create(
            user=self.user_business,
            type='business'
        )
        self.profile_business_2 = UserProfile.objects.create(
            user=self.user_business_2,
            type='business'
        )

    def test_profile_get_authenticated(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('profile-detail', kwargs={'pk': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_profile_get_unauthenticated(self):
        url = reverse('profile-detail', kwargs={'pk': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_get_not_found(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('profile-detail', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_profile(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('profile-detail', kwargs={'pk': self.user.id})
        update_user_data = UPDATE_USER_DATA
        response = self.client.patch(url, update_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(user_profile.location, 'Berlin')

    def test_patch_profile_unauthenticated(self):
        url = reverse('profile-detail', kwargs={'pk': self.user.id})
        response = self.client.patch(url, UPDATE_USER_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_profile_forbidden(self):
        other_user = User.objects.create_user(
            username='otheruser', password='testpass')
        self.client.force_authenticate(user=other_user)
        url = reverse('profile-detail', kwargs={'pk': self.user.id})
        response = self.client.patch(url, UPDATE_USER_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_profile_not_found(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('profile-detail', kwargs={'pk': 999999})
        response = self.client.patch(url, UPDATE_USER_DATA, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_profiles_business_user(self):
        self.client.force_authenticate(user=self.user)

        url = reverse('profile-business-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[1]['user'], self.user_business_2.id)

    def test_get_profiles_customer_user(self):
        self.client.force_authenticate(user=self.user)

        url = reverse('profile-customer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.user.id)
