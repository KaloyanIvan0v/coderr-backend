from core_app.models import UserProfile
from django.contrib.auth.models import User


def create_user(username):
    return User.objects.create_user(
        username=username,
        email=f"{username}@example.com",
        password="password123"
    )


def create_user_profile(user, type):
    return UserProfile.objects.create(
        user=user,
        type=type
    )


TEST_USER_DATA = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123"
}

UPDATE_USER_DATA = {
    'first_name': 'Updated',
    'last_name': 'User',
    'location': 'Berlin',
    'tel': '123456789',
    'description': 'Test description'
}
