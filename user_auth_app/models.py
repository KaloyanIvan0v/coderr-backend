import os
import uuid
from django.db import models
from django.contrib.auth.models import User


def profile_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('profile_images', filename)


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='main_user')
    type = models.CharField(max_length=255, blank=True)
    file = models.ImageField(
        upload_to=profile_image_path,
        default='profile_images/default_profile.png',
        blank=True,
        null=True
    )
    location = models.CharField(max_length=255, blank=True)
    tel = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
