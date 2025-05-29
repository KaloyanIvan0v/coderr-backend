# # core_app/tests/test_filters.py
# from django.test import TestCase
# from rest_framework.exceptions import ValidationError
# from core_app.api.filters import OfferFilter
# from core_app.models import Offer, OfferDetails
# from .test_helper.user_test_helper import create_user, create_user_profile


# class OfferFilterTests(TestCase):
#     def setUp(self):
#         self.business_user = create_user("business_user")
#         self.business_profile = create_user_profile(
#             self.business_user, "business")

#         # Erstelle Test-Offers mit verschiedenen Preisen und Lieferzeiten
#         self.offer1 = Offer.objects.create(
#             user=self.business_profile,
#             title="Cheap Offer",
#             description="Test",
#             min_price=50.00,
#             min_delivery_time=3
#         )
#         OfferDetails.objects.create(
#             offer=self.offer1,
#             title="Basic",
#             price=50.00,
#             delivery_time_in_days=3,
#             revisions=1,
#             offer_type="basic"
#         )

#         self.offer2 = Offer.objects.create(
#             user=self.business_profile,
#             title="Expensive Offer",
#             description="Test",
#             min_price=200.00,
#             min_delivery_time=10
#         )
#         OfferDetails.objects.create(
#             offer=self.offer2,
#             title="Premium",
#             price=200.00,
#             delivery_time_in_days=10,
#             revisions=5,
#             offer_type="premium"
#         )

#     def test_min_price_filter_valid(self):
#         """Test min_price Filter mit gültigem Wert"""
#         filter = OfferFilter()
#         queryset = Offer.objects.all()

#         # Filter nach Mindestpreis 100
#         filtered = filter.filter_min_price(queryset, 'min_price', 100)

#         # Nur das teure Angebot sollte übrig bleiben
#         self.assertEqual(filtered.count(), 1)
#         self.assertEqual(filtered.first(), self.offer2)

#     def test_min_price_filter_negative_value(self):
#         """Test min_price Filter mit negativem Wert"""
#         filter = OfferFilter()
#         queryset = Offer.objects.all()

#         with self.assertRaises(ValidationError) as context:
#             filter.filter_min_price(queryset, 'min_price', -10)

#         self.assertIn('min_price', context.exception.detail)
#         self.assertEqual(
#             context.exception.detail['min_price'], 'Darf nicht negativ sein')

#     def test_max_delivery_time_filter_valid(self):
#         """Test max_delivery_time Filter mit gültigem Wert"""
#         filter = OfferFilter()
#         queryset = Offer.objects.all()

#         # Filter nach maximaler Lieferzeit 5 Tage
#         filtered = filter.filter_max_delivery_time(
#             queryset, 'max_delivery_time', 5)

#         # Nur das schnelle Angebot sollte übrig bleiben
#         self.assertEqual(filtered.count(), 1)
#         self.assertEqual(filtered.first(), self.offer1)

#     def test_max_delivery_time_filter_negative_value(self):
#         """Test max_delivery_time Filter mit negativem Wert"""
#         filter = OfferFilter()
#         queryset = Offer.objects.all()

#         with self.assertRaises(ValidationError) as context:
#             filter.filter_max_delivery_time(queryset, 'max_delivery_time', -5)

#         self.assertIn('max_delivery_time', context.exception.detail)

#     def test_creator_id_filter(self):
#         """Test creator_id Filter"""
#         filter = OfferFilter({'creator_id': self.business_profile.user.id})
#         queryset = Offer.objects.all()

#         filtered = filter.qs
#         self.assertEqual(filtered.count(), 2)

#     def test_combined_filters(self):
#         """Test mehrere Filter gleichzeitig"""
#         filter = OfferFilter({
#             'min_price': 40,
#             'max_delivery_time': 15,
#             'creator_id': self.business_profile.user.id
#         })

#         filtered = filter.qs
#         self.assertEqual(filtered.count(), 2)  # Beide erfüllen die Kriterien
