from django.test import TestCase
from rest_framework.exceptions import ValidationError
from core_app.api.filters import OfferFilter
from core_app.models import Offer, OfferDetails
from .test_helper.user_test_helper import create_user, create_user_profile


class OfferFilterTests(TestCase):
    def setUp(self):
        self.business_user = create_user("business_user")
        self.business_profile = create_user_profile(
            self.business_user, "business")

        self.offer1 = Offer.objects.create(
            user=self.business_user,
            title="Cheap Offer",
            description="Test",
            min_price=50.00,
            min_delivery_time=3
        )
        OfferDetails.objects.create(
            offer=self.offer1,
            title="Basic",
            price=50.00,
            delivery_time_in_days=3,
            revisions=1,
            offer_type="basic"
        )

        self.offer2 = Offer.objects.create(
            user=self.business_user,
            title="Expensive Offer",
            description="Test",
            min_price=200.00,
            min_delivery_time=10
        )
        OfferDetails.objects.create(
            offer=self.offer2,
            title="Premium",
            price=200.00,
            delivery_time_in_days=10,
            revisions=5,
            offer_type="premium"
        )

    def test_min_price_filter_valid(self):
        filter = OfferFilter()
        queryset = Offer.objects.all()

        filtered = filter.filter_min_price(queryset, 'min_price', 100)

        self.assertEqual(filtered.count(), 1)
        self.assertEqual(filtered.first(), self.offer2)

    def test_min_price_filter_negative_value(self):

        filter = OfferFilter()
        queryset = Offer.objects.all()

        with self.assertRaises(ValidationError) as context:
            filter.filter_min_price(queryset, 'min_price', -10)

        self.assertIn('min_price', context.exception.detail)
        self.assertEqual(
            context.exception.detail['min_price'], 'Must not be negative')

    def test_max_delivery_time_filter_valid(self):
        filter = OfferFilter()
        queryset = Offer.objects.all()

        filtered = filter.filter_max_delivery_time(
            queryset, 'max_delivery_time', 5)

        self.assertEqual(filtered.count(), 1)
        self.assertEqual(filtered.first(), self.offer1)

    def test_max_delivery_time_filter_negative_value(self):
        filter = OfferFilter()
        queryset = Offer.objects.all()

        with self.assertRaises(ValidationError) as context:
            filter.filter_max_delivery_time(queryset, 'max_delivery_time', -5)

        self.assertIn('max_delivery_time', context.exception.detail)

    def test_creator_id_filter(self):
        filter = OfferFilter({'creator_id': self.business_user.id})
        queryset = Offer.objects.all()

        filtered = filter.qs
        self.assertEqual(filtered.count(), 2)

    def test_combined_filters(self):
        filter = OfferFilter({
            'min_price': 40,
            'max_delivery_time': 15,
            'creator_id': self.business_user.id
        })

        filtered = filter.qs
        self.assertEqual(filtered.count(), 2)
