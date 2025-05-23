import random
from django.utils import timezone
from core_app.models import Review


def create_review(test_case, business_user, reviewer):
    return Review.objects.create(
        business_user=business_user,
        reviewer=reviewer,
        rating=4,
        description="Test description " + str(random.randint(1, 1000)),
        created_at=timezone.now(),
        updated_at=timezone.now()
    )
