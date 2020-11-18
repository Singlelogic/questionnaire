from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """This class gives access to any users to the methods 'GET', 'HEAD', 'OPTIONS',
    all other methods are available only to administrators.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

