from rest_framework import serializers
from django.contrib.auth.models import User
from user_auth_app.models import UserProfile
import os


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', required=False)
    first_name = serializers.CharField(
        source='user.first_name', required=False)
    last_name = serializers.CharField(source='user.last_name', required=False)
    file_url = serializers.SerializerMethodField()
    user = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(), required=False)
    created_at = serializers.DateTimeField(
        read_only=True, format='%Y-%m-%dT%H:%M:%S')

    class Meta:
        model = UserProfile
        fields = ['user', 'username', 'email', 'type', 'first_name', 'last_name', 'file',
                  'file_url', 'location', 'tel', 'description', 'working_hours', 'created_at']
        read_only_fields = ['created_at', 'file_url']

    def get_file_url(self, obj):
        if obj.file:
            return obj.file.url
        return None

    def validate_file(self, value):
        if value:

            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError(
                    "File is too large. Maximum 5MB allowed.")

            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            ext = os.path.splitext(value.name)[1].lower()
            if ext not in valid_extensions:
                raise serializers.ValidationError(
                    "Only JPG, PNG and GIF files are allowed.")

        return value

    def update(self, instance, validated_data):

        user_data = {}

        if 'user' in validated_data and isinstance(validated_data['user'], UserProfile):
            user_data['user'] = validated_data.pop('user')

        if 'user' in validated_data and isinstance(validated_data['user'], dict):
            user_data.update(validated_data.pop('user'))

        user = instance.user
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        if 'email' in user_data:
            user.email = user_data['email']
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class ProfileTypeListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    first_name = serializers.CharField(
        source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all())

    class Meta:
        model = UserProfile
        fields = ['user', 'username',  'first_name', 'last_name', 'file',
                  'type', 'location', 'tel', 'description', 'working_hours']


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    username = serializers.CharField(required=False)
    type = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password',
                  'repeated_password', 'type']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):

        if 'username' not in data or not data['username']:
            base_username = data['email'].split('@')[0]
            username = base_username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            data['username'] = username

        return data

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "This email address is already in use.")
        return value

    def save(self):
        pw = self.validated_data['password']
        repeated_pw = self.validated_data['repeated_password']
        type = self.validated_data.get('type', 'customer')

        if pw != repeated_pw:
            raise serializers.ValidationError({
                'password': 'Passwords must match.'
            })

        account = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'])

        account.set_password(pw)
        account.save()

        UserProfile.objects.create(
            user=account,
            type=type
        )

        return account


class LogInSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False, required=True
    )

    class Meta:
        model = User
        fields = ['username', 'password',]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')

            if not user.check_password(password):
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
