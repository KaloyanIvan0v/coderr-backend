from django.urls import path, include
from rest_framework import routers
from user_auth_app.api.views import RegistrationView, LogInView


urlpatterns = [
    path('registration/',
         RegistrationView.as_view(), name='registration'),
    path('login/',
         LogInView.as_view(), name='login')
]
