from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsBusinessUser(BasePermission):
    def has_permission(self, request, view):
        if not hasattr(request.user, 'main_user') or request.user.main_user.type != 'business':
            raise PermissionDenied(
                "403: Authentifizierter Benutzer ist kein 'business' Profil")
        return True
