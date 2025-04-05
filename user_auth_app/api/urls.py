from django.urls import path, include
from rest_framework import routers
from user_auth_app.api.views import Registration, LogIn


urlpatterns = [
    path('registration//',
         Registration.as_view(), name='registration'),
    path('login//',
         LogIn.as_view(), name='login')
]
