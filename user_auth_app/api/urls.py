from django.urls import path, include
from rest_framework import routers
from user_auth_app.api.views import RegistrationView, LogInView
from .views import ProfileBusinessListView, ProfileCustomerListView, ProfileView


urlpatterns = [
    path("profile/<int:pk>/", ProfileView.as_view(), name="profile-detail"),
    path("profiles/customer/", ProfileCustomerListView.as_view(),
         name="profile-customer-list"),
    path("profiles/business/", ProfileBusinessListView.as_view(),
         name="profile-business-list"),
    path('registration/',
         RegistrationView.as_view(), name='registration'),
    path('login/',
         LogInView.as_view(), name='login')
]
