from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from core_app.models import Offer, Order, Rating, OfferDetails, OfferFeatures
from .serializers import ProfileDetailSerializer, OfferSerializer, \
    OfferDetailSerializer, OfferFeaturesSerializer, OfferListSerializer, \
    OrderSerializer, OrderCountSerializer, OrderCompletedCountSerializer
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
    queryset = Order.objects.none()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user

        try:
            user_profile = user.main_user
        except:
            return Order.objects.none()

        return Order.objects.filter(
            Q(customer_user=user_profile) |
            Q(business_user=user_profile)
        ).order_by('-created_at')


class OrderCountView(APIView):
    queryset = Order.objects.none()
    serializer_class = OrderCountSerializer

    def get(self, request):
        user = self.request.user

        try:
            user_profile = user.main_user
        except:
            return Response({"order_count": 0})

        # Filter for in-progress orders where the user is either customer or business
        order_count = Order.objects.filter(
            Q(customer_user=user_profile) |
            Q(business_user=user_profile),
            status="in_progress"  # Nur Orders mit Status "in_progress"
        ).count()  # Zählt die Anzahl statt die Orders zurückzugeben

        return Response({"order_count": order_count})


class OrderCompletedCount(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderCompletedCountSerializer

    def get(self, request):
        user = self.request.user

        try:
            user_profile = user.main_user
        except:
            return Response({"order_count": 0})

        # Filter for completed orders where the user is either customer or business
        order_count = Order.objects.filter(
            Q(customer_user=user_profile) |
            Q(business_user=user_profile),
            status="completed"  # Nur Orders mit Status "completed"
        ).count()  # Zählt die Anzahl statt die Orders zurückzugeben

        return Response({"order_count": order_count})


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
