from django.urls import path, include
from rest_framework import routers
from core_app.api.views import OrderViewSet, OfferViewSet, ReviewViewSet, \
    OrderCountView, OrderCompletedCount, BaseInfoView


router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet)
router.register(r'offers', OfferViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('completed-order-count/<business_user_id>/',
         OrderCompletedCount.as_view(), name='order-completed-count'),
    path('order-count/<business_user_id>/',
         OrderCountView.as_view(), name='order-count'),
    path("base-info/", BaseInfoView.as_view(), name="base-info")
]
