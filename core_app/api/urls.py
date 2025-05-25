from django.urls import path, include
from rest_framework import routers
from core_app.api.views import base_info_view

from core_app.api.views import OrderViewSet, OfferViewSet, ReviewViewSet, \
    OrderCountView, CompletedOrderCountView, base_info_view, \
    OfferDetailViewSet


router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'offers', OfferViewSet, basename='offers')
router.register(r'offerdetails', OfferDetailViewSet,
                basename='offerdetails')
router.register(r'reviews', ReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(router.urls)),
    path('completed-order-count/<int:business_user_id>/',
         CompletedOrderCountView.as_view(), name='completed-order-count'),
    path('order-count/<int:business_user_id>/',
         OrderCountView.as_view(), name='order-count'),
    path("base-info/", base_info_view, name="base-info"),
]
