from rest_framework import viewsets
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from core_app.models import Offer, Order, Rating
from rest_framework.response import Response


class ProfileDetailView(RetrieveAPIView):
    pass


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
    def get(self, request):
        data = {
            "review_count": 10,
            "average_rating": 4.6,
            "business_profile_count": 45,
            "offer_count": 150
        }
        return Response(data)
