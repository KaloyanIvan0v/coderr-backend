from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from core_app.models import Offer, Order, Rating


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
    pass
