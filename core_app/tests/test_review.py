from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from core_app.models import Review
from .test_helper.user_test_helper import create_user, create_user_profile
from .test_helper.review_test_helper import create_review, TEST_REVIEW_DATA


class ReviewViewTests(APITestCase):
    def setUp(self):
        self.user = create_user("tomas_customer")
        self.profile = create_user_profile(self.user, "customer")

        self.business_user = create_user("markus_business")
        self.business_profile = create_user_profile(
            self.business_user, "business")

        self.reviewer = create_user("linus_reviewer")
        self.reviewer_profile = create_user_profile(
            self.reviewer, "customer")

        self.review = create_review(
            self, self.business_user, self.reviewer)

    def test_get_reviews(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('reviews-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['rating'], 4)

    def test_get_reviews_unauthenticated(self):
        url = reverse('reviews-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_review(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('reviews-list')
        data = {
            "business_user": self.business_user.id,
            "rating": 5,
            "description": "Great service!"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 2)
        self.assertEqual(Review.objects.last().reviewer, self.user)

    def test_create_review_bad_request_review_already_exists(self):
        self.client.force_authenticate(user=self.reviewer)
        url = reverse('reviews-list')
        data = {
            "business_user": self.business_user.id,
            "rating": 5,
            "description": "Trying to review again"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_review_unauthenticated(self):
        url = reverse('reviews-list')
        data = TEST_REVIEW_DATA
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Review.objects.count(), 1)

    def test_update_review(self):
        self.client.force_authenticate(user=self.reviewer)
        url = reverse('reviews-detail', args=[self.review.id])
        data = {
            "rating": 5,
            "description": "Updated review"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.last().rating, 5)
        self.assertEqual(Review.objects.last().description, "Updated review")

    def test_update_review_bad_request_invalid_data(self):
        self.client.force_authenticate(user=self.reviewer)
        url = reverse('reviews-detail', args=[self.review.id])
        data = {
            "rating": 6,
            "description": "Updated review"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_review_unauthenticated(self):
        url = reverse('reviews-detail', args=[self.review.id])
        data = {
            "rating": 5,
            "description": "Updated review"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_review_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('reviews-detail', args=[self.review.id])
        data = {
            "rating": 5,
            "description": "Updated review"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_review(self):
        self.client.force_authenticate(user=self.reviewer)
        url = reverse('reviews-detail', args=[self.review.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Review.objects.count(), 0)

    def test_delete_review_unauthenticated(self):
        url = reverse('reviews-detail', args=[self.review.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_review_forbidden(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('reviews-detail', args=[self.review.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_review_not_found(self):
        self.client.force_authenticate(user=self.reviewer)
        url = reverse('reviews-detail', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
