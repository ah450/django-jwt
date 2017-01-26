from rest_framework import permissions

class AuthenticatedPermission(permissions.BasePermission):
    """
    Permission that only allows authenticated users.
    Author: Ahmed H. Ismail
    """

    def has_permission(self, request, *args, **kwargs):
        return not request.user.is_anonymous()