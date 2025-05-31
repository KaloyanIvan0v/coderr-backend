from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from user_auth_app.models import UserProfile
from user_auth_app.api.serializers import RegistrationSerializer, LogInSerializer
from .serializers import ProfileSerializer, ProfileTypeListSerializer


class ProfileView(RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_object(self):
        user_id = self.kwargs.get('pk')
        new_user = get_object_or_404(UserProfile, user__id=user_id)
        return new_user

    def patch(self, request, pk):
        user_profile = self.get_object()

        if request.user.id != user_profile.user.id:
            return Response({"detail": "You are not authorized to edit this profile."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(
            user_profile, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


class ProfileBusinessListView(ListAPIView):
    queryset = UserProfile.objects.filter(type="business")
    serializer_class = ProfileTypeListSerializer


class ProfileCustomerListView(ListAPIView):
    queryset = UserProfile.objects.filter(type="customer")
    serializer_class = ProfileTypeListSerializer


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'username': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.id
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
            return Response(data, status=status.HTTP_400_BAD_REQUEST)


class LogInView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LogInSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'user_id': user.id

            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
