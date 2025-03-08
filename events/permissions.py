from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    """
    Allows access only to admin users (staff users).
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
