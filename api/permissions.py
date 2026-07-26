from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Allow read-only access to everyone permitted by the view.

    Object modification is allowed only for the object's owner.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return getattr(obj, "user", None) == request.user