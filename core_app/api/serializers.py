from rest_framework import serializers
from user_auth_app.models import UserProfile
from core_app.models import Offer, OfferDetails, OfferFeatures, \
    Review, Order, OrderFeatures
from core_app.models import OfferDetails
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone


class OfferFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferFeatures
        fields = ['feature']

    def to_internal_value(self, data):
        if isinstance(data, str):
            return {'feature': data}
        return super().to_internal_value(data)

    def to_representation(self, instance):
        return instance.feature


class OfferDetailSerializer(serializers.ModelSerializer):
    features = OfferFeaturesSerializer(many=True)

    class Meta:
        model = OfferDetails
        user = serializers.PrimaryKeyRelatedField(
            queryset=UserProfile.objects.all())
        fields = ['id', 'offer', 'title', 'revisions', 'delivery_time_in_days',
                  'price', 'features', 'offer_type']
        extra_kwargs = {
            'offer': {'required': False}
        }

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

        if features_data:

            instance.features.all().delete()

            for feature_data in features_data:
                OfferFeatures.objects.create(
                    offer_detail=instance, **feature_data)

        return instance


class OfferDetailReferenceSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = OfferDetails
        fields = ['id', 'url']

    def get_url(self, obj):
        return f"/offerdetails/{obj.id}/"

# Create a separate serializer for listing offers


class OfferListSerializer(serializers.ModelSerializer):
    details = OfferDetailReferenceSerializer(many=True, read_only=True)
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description',
                  'created_at', 'updated_at', 'details', 'min_price',
                  'min_delivery_time', 'user_details']

    def get_user_details(self, obj):
        return {
            'first_name': obj.user.user.first_name,
            'last_name': obj.user.user.last_name,
            'username': obj.user.user.username
        }


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)

    class Meta:
        model = Offer
        fields = ['id', 'user', 'title', 'image', 'description',
                  'created_at', 'updated_at', 'details', 'min_price', 'min_delivery_time']
        extra_kwargs = {'id': {'read_only': True}}

    def validate(self, attrs):
        unknown_fields = set(self.initial_data.keys()) - \
            set(self.fields.keys())
        if unknown_fields:
            raise serializers.ValidationError(
                f"Unknown fields: {', '.join(unknown_fields)}")
        return super().validate(attrs)

    def get_user(self, obj):
        return obj.user.id

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


class OrderFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderFeatures
        fields = ['feature']

    def to_internal_value(self, data):
        if isinstance(data, str):
            return {'feature': data}
        return super().to_internal_value(data)

    def to_representation(self, instance):
        return instance.feature


class OrderSerializer(serializers.ModelSerializer):
    offer_detail_id = serializers.IntegerField(
        write_only=True)
    features = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_user', 'business_user', 'title', 'revisions',
                  'delivery_time_in_days', 'price', 'offer_type', 'status',
                  'created_at', 'updated_at', 'features', 'offer_detail_id']

        read_only_fields = ['id', 'customer_user', 'business_user', 'title', 'revisions',
                            'delivery_time_in_days', 'price', 'offer_type',
                            'status', 'created_at', 'updated_at', 'features']

    def create(self, validated_data):
        offer_detail_id = validated_data.pop('offer_detail_id')

        try:
            offer_detail = OfferDetails.objects.get(id=offer_detail_id)
            print(offer_detail)
        except OfferDetails.DoesNotExist:
            raise serializers.ValidationError(
                "OfferDetail mit dieser ID existiert nicht."
            )

        customer_user = self.context['request'].user.main_user
        order = Order.objects.create(
            customer_user=customer_user,
            business_user=offer_detail.offer.user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            offer_type=offer_detail.offer_type,
            status='in_progress',
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

        if hasattr(offer_detail, 'features'):
            for feature in offer_detail.features.all():
                OrderFeatures.objects.create(
                    order=order,
                    feature=feature.feature
                )

        return order


class OrderCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_count']


class CompletedOrderCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['completed_order_count']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating', 'description',
                  'created_at', 'updated_at']
