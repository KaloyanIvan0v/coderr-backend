from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
        if not hasattr(request.user, 'main_user') or request.user.main_user.type != 'business':
            raise PermissionDenied(
                "403: Authenticated user is not a business user")
        return True


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id
