import os
import uuid
from django.db import models
from user_auth_app.models import UserProfile
from django.core.validators import MinValueValidator, MaxValueValidator
from user_auth_app.models import User


def offer_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('offers', filename)


class Offer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    image = models.ImageField(
        upload_to=offer_image_path, null=True, blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_price = models.DecimalField(
        max_digits=10, decimal_places=2)
    min_delivery_time = models.IntegerField()

    def __str__(self):
        return self.title


class OfferDetails(models.Model):
    offer = models.ForeignKey(
        Offer, related_name='details', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_type = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class OfferFeatures(models.Model):
    offer_detail = models.ForeignKey(
        OfferDetails, related_name='features', on_delete=models.CASCADE)
    feature = models.CharField(max_length=255)

    def __str__(self):
        return self.feature


class Order(models.Model):
    customer_user = models.ForeignKey(
        User, related_name='customer_orders', on_delete=models.CASCADE)
    business_user = models.ForeignKey(
        User, related_name='business_orders', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    offer_type = models.CharField(max_length=50)
    status = models.CharField(
        max_length=20,  default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class OrderFeatures(models.Model):
    order = models.ForeignKey(
        Order, related_name='features', on_delete=models.CASCADE)
    feature = models.CharField(max_length=255)

    def __str__(self):
        return self.feature


class Review(models.Model):
    business_user = models.ForeignKey(
        User, related_name='received_ratings', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(
        User, related_name='given_ratings', on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rating {self.rating}/5 from {self.reviewer} to {self.business_user}"
