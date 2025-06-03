from django.contrib.auth.models import User
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from core_app.models import Offer, Order, Review, OfferDetails, OfferFeatures
from .serializers import OfferSerializer, \
    OfferDetailSerializer, OfferFeaturesSerializer, OfferListSerializer, \
    OrderSerializer, OrderCountSerializer, CompletedOrderCountSerializer, \
    ReviewSerializer, BaseInfoSerializer
from user_auth_app.models import UserProfile
from .filters import OfferFilter
from .permissions.main_permissions import IsBusinessUser, IsOwner, IsCustomerUser


class OfferPageViewPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    page_query_param = 'page'


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all().order_by('-created_at')
    pagination_class = OfferPageViewPagination
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_class = OfferFilter
    search_fields = ['title', 'description']
    ordering_fields = ['updated_at', 'min_price']
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsBusinessUser()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsBusinessUser(), IsOwner()]
        return [AllowAny()]

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
        elif self.action == 'create':
            return [IsAuthenticated(), IsCustomerUser()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsBusinessUser()]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        user = self.request.user

        if user.is_staff or user.is_superuser:
            return Order.objects.all().order_by('-created_at')

        return Order.objects.filter(
            Q(customer_user=user) |
            Q(business_user=user)
        ).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={
                                         'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class OrderCountView(APIView):
    queryset = Order.objects.none()
    serializer_class = OrderCountSerializer

    def get(self, request, business_user_id):
        business_user = get_object_or_404(User, id=business_user_id)
        order_count = Order.objects.filter(
            business_user=business_user,
            status="in_progress"
        ).count()

        return Response({"order_count": order_count})


class CompletedOrderCountView(APIView):
    queryset = Order.objects.all()
    serializer_class = CompletedOrderCountSerializer

    def get(self, request, business_user_id):
        business_user = get_object_or_404(User, id=business_user_id)
        order_count = Order.objects.filter(
            business_user=business_user,
            status="completed"
        ).count()

        return Response({"completed_order_count": order_count})


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by('-updated_at')
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['business_user', 'reviewer']
    ordering_fields = ['updated_at', 'rating']
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsCustomerUser()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsCustomerUser(), IsOwner()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsCustomerUser(), IsOwner()]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()

        business_user_id = self.request.query_params.get('business_user_id')
        if business_user_id:
            queryset = queryset.filter(business_user__id=business_user_id)

        reviewer_id = self.request.query_params.get('reviewer_id')
        if reviewer_id:
            queryset = queryset.filter(reviewer__id=reviewer_id)

        return queryset


@api_view(['GET'])
@permission_classes([AllowAny])
def base_info_view(request):
    try:
        review_count = Review.objects.count()

        avg_rating = Review.objects.aggregate(
            avg_rating=Avg('rating')
        )['avg_rating']
        average_rating = round(avg_rating, 1) if avg_rating else 0.0

        business_profile_count = UserProfile.objects.filter(
            type='business'
        ).count()

        offer_count = Offer.objects.count()

        data = {
            "review_count": review_count,
            "average_rating": average_rating,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count
        }

        serializer = BaseInfoSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception:
        return Response(
            {"error": "Internal Server Error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
