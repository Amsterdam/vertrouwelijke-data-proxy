from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class IsFpMdw(BasePermission):
    """Permission check, wrapped in a DRF permissions adapter"""

    message = "Required scope not given."

    def has_permission(self, request, view):
        """Check whether the user has fp_mdw scope"""
        # When the access is granted, this skips going into the authorization middleware.
        # This is solely done to avoid incorrect log messages of "access granted",
        # because additional checks may still deny access.
        needed_scope = frozenset({"FP/MDW"})
        user_scopes = set(request.get_token_scopes)
        if user_scopes.issuperset(needed_scope):
            return True

        if not request.is_authorized_for(*needed_scope):
            # Raise explicit error to provide error message
            raise PermissionDenied(self.message)
        else:
            return True

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
