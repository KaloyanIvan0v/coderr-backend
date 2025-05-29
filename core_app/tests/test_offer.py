from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from core_app.models import Offer, OfferDetails, OfferFeatures
from .test_helper.offer_test_helper import OFFER_DATA, OFFER_DATA_CREATE, OFFER_DATA_CREATE_DETAIL
from .test_helper.user_test_helper import create_user, create_user_profile


class OfferViewTests(APITestCase):
    def setUp(self):

        self.user = create_user("tomas_customer")
        self.profile = create_user_profile(self.user, "customer")

        self.business_user = create_user("markus_business")
        self.business_profile = create_user_profile(
            self.business_user, "business")

        self.business_user_2 = create_user("linus_business")
        self.business_profile_2 = create_user_profile(
            self.business_user_2, "business")

        offer_data = OFFER_DATA_CREATE.copy()
        offer_data['user'] = self.business_user

        self.offer = Offer.objects.create(**offer_data)

        for detail_data in OFFER_DATA_CREATE_DETAIL['details']:
            features = detail_data.pop('features', [])
            detail = OfferDetails.objects.create(
                offer=self.offer, **detail_data)

            for feature in features:
                OfferFeatures.objects.create(
                    offer_detail=detail, feature=feature)

    def test_get_offers(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('offers-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Multipaket")

    def test_get_offers_bad_request(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('offers-list') + '?min_price=abc'

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_offer(self):
        self.client.force_authenticate(user=self.business_user)
        url = reverse('offers-list')
        data = OFFER_DATA.copy()
        data['user'] = self.business_user.id
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 2)
        new_offer = Offer.objects.latest('created_at')
        self.assertEqual(new_offer.description,
                         "Ein umfassendes Grafikdesign-Paket für Unternehmen.")

    def test_create_offer_invalid_request(self):
        self.client.force_authenticate(user=self.business_user)
        url = reverse('offers-list')
        data = OFFER_DATA.copy()
        data['title'] = {"apm", "cham", "da"}
        data['user'] = self.business_user.id
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_offer_unauthorized(self):
        url = reverse('offers-list')
        data = OFFER_DATA.copy()
        data['user'] = self.user.id
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_offer_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('offers-list')
        data = OFFER_DATA.copy()
        data['user'] = self.user.id
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_offer(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('offers-detail', kwargs={'pk': self.offer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Multipaket")

    def test_get_offer_unauthorized(self):
        url = reverse('offers-detail', kwargs={'pk': self.offer.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_offer_not_found(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('offers-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_offer(self):
        self.client.force_authenticate(user=self.business_user)
        url = reverse('offers-detail', kwargs={'pk': self.offer.id})
        response = self.client.patch(
            url, {'title': 'Updated Offer'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Offer')

    def test_patch_offer_unknown_field(self):
        self.client.force_authenticate(user=self.business_user)
        url = reverse('offers-detail', kwargs={'pk': self.offer.id})
        response = self.client.patch(
            url, {'tittttle': 'Updated Offer'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_offer_unauthorized(self):
        url = reverse('offers-detail', kwargs={'pk': self.offer.id})
        response = self.client.patch(
            url, {'title': 'Updated Offer'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_patch_offer_forbidden(self):
        self.client.force_authenticate(user=self.business_user_2)
        url = reverse('offers-detail', kwargs={'pk': self.offer.id})
        response = self.client.patch(
            url, {'title': 'Updated Offer'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_patch_offer_not_found(self):
        self.client.force_authenticate(user=self.business_user)
        url = reverse('offers-detail', kwargs={'pk': 9999})
        response = self.client.patch(
            url, {'title': 'Updated Offer'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_offer(self):
        self.client.force_authenticate(user=self.business_user)
        url = reverse('offers-detail', kwargs={'pk': self.offer.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Offer.objects.count(), 0)

    def test_delete_offer_unauthorized(self):
        url = reverse('offers-detail', kwargs={'pk': self.offer.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_offer_forbidden(self):
        self.client.force_authenticate(user=self.business_user_2)
        url = reverse('offers-detail', kwargs={'pk': self.offer.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_offer_not_found(self):
        self.client.force_authenticate(user=self.business_user)
        url = reverse('offers-detail', kwargs={'pk': 9999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_offerdetails(self):
        self.client.force_authenticate(user=self.user)
        detail = self.offer.details.first()
        self.assertIsNotNone(detail, "no detail found")
        url = reverse('offerdetails-detail', kwargs={'pk': detail.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_offerdetails_unauthorized(self):
        url = reverse('offerdetails-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_offerdetails_not_found(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('offerdetails-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
