from django.urls import path, include
from rest_framework import routers


from core_app.api.views import OrderViewSet, OfferViewSet, ReviewViewSet, \
    OrderCountView, CompletedOrderCountView, BaseInfoView, ProfileView, \
    OfferDetailViewSet, ProfileCustomerListView, ProfileBusinessListView


router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'offers', OfferViewSet, basename='offers')
router.register(r'offerdetails', OfferDetailViewSet,
                basename='offerdetails')
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile-detail"),
    path("profiles/customer/", ProfileCustomerListView.as_view(),
         name="profile-customer-list"),
    path("profiles/business/", ProfileBusinessListView.as_view(),
         name="profile-business-list"),
    path('completed-order-count/<int:business_user_id>/',
         CompletedOrderCountView.as_view(), name='order-completed-count'),
    path('order-count/<int:business_user_id>/',
         OrderCountView.as_view(), name='order-count'),
    path("base-info/", BaseInfoView.as_view(), name="base-info"),

]
