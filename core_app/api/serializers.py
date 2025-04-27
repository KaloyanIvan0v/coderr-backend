from rest_framework import serializers
from user_auth_app.models import UserProfile
from core_app.models import Offer, OfferDetails, OfferFeatures


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


class OfferFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferFeatures
        fields = ['id', 'feature']


class OfferDetailSerializer(serializers.ModelSerializer):
    features = OfferFeaturesSerializer(many=True)

    class Meta:
        model = OfferDetails
        fields = ['id', 'offer', 'title', 'revisions', 'delivery_time_in_days',
                  'price', 'features', 'offer_type']


class OfferSerializer(serializers.ModelSerializer):

    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description',
                  'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time']
