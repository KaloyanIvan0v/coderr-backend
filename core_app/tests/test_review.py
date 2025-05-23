from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from core_app.models import Review

from .test_helper.user_test_helper import create_user, create_user_profile
from .test_helper.review_test_helper import create_review


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
            self, self.business_profile, self.reviewer_profile)

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
