from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from core_app.models import Offer, Order, Rating
from rest_framework.response import Response
from .serializers import ProfileDetailSerializer
from user_auth_app.models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class ProfileDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = UserProfile.objects.all()
    serializer_class = ProfileDetailSerializer

    def get_object(self):
        user_id = self.kwargs.get('pk')
        new_user = get_object_or_404(UserProfile, user__id=user_id)
        return new_user


class ProfileUpdateView(UpdateAPIView):
    pass


class ProfileBusinessListView(ListAPIView):
    pass


class ProfileCustomerListView(ListAPIView):
    pass


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()


class OfferDetailView(APIView):
    pass


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()


class OrderCountView(APIView):
    pass


class OrderCompletedCount(APIView):
    pass


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()


class BaseInfoView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = {
            "review_count": 10,
            "average_rating": 4.6,
            "business_profile_count": 45,
            "offer_count": 150
        }
        return Response(data)
