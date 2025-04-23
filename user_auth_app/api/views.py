from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from user_auth_app.models import UserProfile
from user_auth_app.api.serializers import RegistrationSerializer, LogInSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


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
        else:
            data = serializer.errors
        return Response(data)


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
        else:
            data = serializer.errors
        return Response(data)
