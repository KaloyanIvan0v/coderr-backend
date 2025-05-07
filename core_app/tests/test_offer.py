from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.test import APITestCase
from rest_framework import status

from core_app.models import UserProfile, Offer, OfferDetails, OfferFeatures
from .test_data.offer_data import GRAPHIC_DESIGN_OFFER_DATA, GRAPHIC_DESIGN_OFFER_DATA_CREATE, GRAPHIC_DESIGN_OFFER_DATA_CREATE_DETAIL
from .test_data.user_data import TEST_USER_DATA


class OfferViewTests(APITestCase):
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
        offer_data = GRAPHIC_DESIGN_OFFER_DATA_CREATE.copy()
        offer_data['user'] = self.profile
        self.offer = Offer.objects.create(**offer_data)

        for detail_data in GRAPHIC_DESIGN_OFFER_DATA_CREATE_DETAIL['details']:
            features = detail_data.pop('features', [])
            detail = OfferDetails.objects.create(
                offer=self.offer, **detail_data)

            for feature in features:
                OfferFeatures.objects.create(
                    offer_detail=detail, feature=feature)

    def test_create_offer(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('offers-list')
        data = GRAPHIC_DESIGN_OFFER_DATA.copy()
        data['user'] = self.user.id
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 2)
        new_offer = Offer.objects.latest('created_at')
        self.assertEqual(new_offer.description,
                         "Ein umfassendes Grafikdesign-Paket für Unternehmen.")

    def test_get_offers(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('offers-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Multipaket")

    def test_get_offer(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('offers-detail', kwargs={'pk': self.offer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Multipaket")

    def test_patch_offer(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('offers-detail', kwargs={'pk': self.offer.id})
        response = self.client.patch(
            url, {'title': 'Updated Offer'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Offer')

    def test_delete_offer(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('offers-detail', kwargs={'pk': self.offer.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Offer.objects.count(), 0)

    def test_get_offerdetails(self):
        self.client.force_authenticate(user=self.user)
        detail = self.offer.details.first()
        self.assertIsNotNone(detail, "Es wurde kein OfferDetail gefunden.")
        url = reverse('offerdetails-detail', kwargs={'pk': detail.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data['features'][0], "Logo Design")
        # self.assertEqual(response.data['features'][1], "Visitenkarte")
