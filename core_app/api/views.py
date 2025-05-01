from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from core_app.models import Offer, Order, Rating, OfferDetails, OfferFeatures
from .serializers import ProfileDetailSerializer, OfferSerializer, \
    OfferDetailSerializer, OfferFeaturesSerializer, OfferListSerializer
from user_auth_app.models import UserProfile


class OfferPageViewPagination(PageNumberPagination):
    page_size = 6


class ProfileDetailView(RetrieveAPIView):
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
    queryset = Offer.objects.all().order_by('-created_at')
    pagination_class = OfferPageViewPagination

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return OfferSerializer
        return OfferListSerializer


class OfferDetailViewSet(viewsets.ModelViewSet):
    queryset = OfferDetails.objects.all()
    serializer_class = OfferDetailSerializer


class OfferFeaturesViewSet(viewsets.ModelViewSet):
    queryset = OfferFeatures.objects.all()
    serializer_class = OfferFeaturesSerializer


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
