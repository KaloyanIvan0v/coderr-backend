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
    message = "You do not have permission to access this resource."

    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id


class IsCustomerUser(BasePermission):
    message = "Authenticated user is not a customer user"

    def has_permission(self, request, view):
        return (
            hasattr(request.user, 'main_user') and
            getattr(request.user.main_user, 'type', None) == 'customer'
        )
