from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


from core_app.models import Offer, Order, Review, OfferDetails, OfferFeatures
from .serializers import OfferSerializer, \
    OfferDetailSerializer, OfferFeaturesSerializer, OfferListSerializer, \
    OrderSerializer, OrderCountSerializer, CompletedOrderCountSerializer, \
    ReviewSerializer
from user_auth_app.models import UserProfile
from .filters import OfferFilter


class OfferPageViewPagination(PageNumberPagination):
    page_size = 6


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all().order_by('-created_at')
    pagination_class = OfferPageViewPagination
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']

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

    def get_permissions(self):
        if self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return Order.objects.all().order_by('-created_at')

        try:
            user_profile = user.main_user
        except AttributeError:
            return Order.objects.none()

        return Order.objects.filter(
            Q(customer_user=user_profile) |
            Q(business_user=user_profile)
        ).order_by('-created_at')


class OrderCountView(APIView):
    queryset = Order.objects.none()
    serializer_class = OrderCountSerializer

    def get(self, request, business_user_id):
        user_profile = get_object_or_404(
            UserProfile, user__id=business_user_id)
        order_count = Order.objects.filter(
            business_user=user_profile,
            status="in_progress"
        ).count()

        return Response({"order_count": order_count})


class CompletedOrderCountView(APIView):
    queryset = Order.objects.all()
    serializer_class = CompletedOrderCountSerializer

    def get(self, request, business_user_id):
        user = get_object_or_404(User, id=business_user_id)
        user_profile = get_object_or_404(UserProfile, user=user)
        order_count = Order.objects.filter(
            business_user=user_profile,
            status="completed"
        ).count()

        return Response({"order_count": order_count})


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


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
