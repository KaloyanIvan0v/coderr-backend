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
        user = serializers.PrimaryKeyRelatedField(
            queryset=UserProfile.objects.all())
        fields = ['id', 'offer', 'title', 'revisions', 'delivery_time_in_days',
                  'price', 'features', 'offer_type']

    def create(self, validated_data):
        features_data = validated_data.pop('features')
        offer_detail = OfferDetails.objects.create(**validated_data)

        for feature_data in features_data:
            OfferFeatures.objects.create(
                offer_detail=offer_detail, **feature_data)

        return offer_detail

    def update(self, instance, validated_data):
        features_data = validated_data.pop('features', [])
        instance.title = validated_data.get('title', instance.title)
        instance.revisions = validated_data.get(
            'revisions', instance.revisions)
        instance.delivery_time_in_days = validated_data.get(
            'delivery_time_in_days', instance.delivery_time_in_days)
        instance.price = validated_data.get('price', instance.price)
        instance.offer_type = validated_data.get(
            'offer_type', instance.offer_type)
        instance.save()

        # Handle features
        if features_data:
            # Optional: remove existing features not included in the update
            instance.features.all().delete()

            for feature_data in features_data:
                OfferFeatures.objects.create(
                    offer_detail=instance, **feature_data)

        return instance


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description',
                  'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time']

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        offer = Offer.objects.create(**validated_data)

        for detail_data in details_data:
            features_data = detail_data.pop('features', [])
            offer_detail = OfferDetails.objects.create(
                offer=offer, **detail_data)

            for feature_data in features_data:
                OfferFeatures.objects.create(
                    offer_detail=offer_detail, **feature_data)

        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', [])
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.min_price = validated_data.get(
            'min_price', instance.min_price)
        instance.min_delivery_time = validated_data.get(
            'min_delivery_time', instance.min_delivery_time)
        instance.image = validated_data.get('image', instance.image)
        instance.save()

        if details_data:

            instance.details.all().delete()

            for detail_data in details_data:
                features_data = detail_data.pop('features', [])
                offer_detail = OfferDetails.objects.create(
                    offer=instance, **detail_data)

                for feature_data in features_data:
                    OfferFeatures.objects.create(
                        offer_detail=offer_detail, **feature_data)

        return instance
