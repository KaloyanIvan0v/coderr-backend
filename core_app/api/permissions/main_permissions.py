from rest_framework.permissions import BasePermission


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
        if hasattr(obj, 'user'):
            return obj.user.id == request.user.id
        elif hasattr(obj, 'reviewer'):
            return obj.reviewer.id == request.user.id
        elif hasattr(obj, 'customer_user'):
            return obj.customer_user.id == request.user.id
        return False


class IsCustomerUser(BasePermission):
    message = "Authenticated user is not a customer user"

    def has_permission(self, request, view):
        return (
            hasattr(request.user, 'main_user') and
            getattr(request.user.main_user, 'type', None) == 'customer'
        )
