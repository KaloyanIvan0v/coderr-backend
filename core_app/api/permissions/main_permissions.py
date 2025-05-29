from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsBusinessUser(BasePermission):
    message = "Authenticated user is not a business user"

    def has_permission(self, request, view):
        return (
            hasattr(request.user, 'main_user') and
            getattr(request.user.main_user, 'type', None) == 'business'
        )


class IsOwner(BasePermission):
    message = "You can only modify your own content"

    def has_object_permission(self, request, view, obj):
        # Handle different model types
        if hasattr(obj, 'user'):
            # For models with 'user' field (like Offer)
            return obj.user.id == request.user.id
        elif hasattr(obj, 'reviewer'):
            # For Review model
            return obj.reviewer.id == request.user.id
        elif hasattr(obj, 'customer_user'):
            # For Order model (if customer is updating)
            return obj.customer_user.id == request.user.id

        return False


class IsCustomerUser(BasePermission):
    message = "Authenticated user is not a customer user"

    def has_permission(self, request, view):
        return (
            hasattr(request.user, 'main_user') and
            getattr(request.user.main_user, 'type', None) == 'customer'
        )
