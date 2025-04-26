from rest_framework import serializers
from user_auth_app.models import UserProfile


class ProfileDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    first_name = serializers.CharField(
        source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'user_type', 'first_name', 'last_name', 'profile_image',
                  'location', 'tel', 'description', 'working_hours', 'created_at']
