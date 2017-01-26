from rest_framework import permissions

class VeriefiedPermission(permissions.BasePermission):
    """
    Permission that only allows users that have been manually verified.
    """

    def has_permission(self, request, *args, **kwargs):
        return request.user.profile.manually_verified