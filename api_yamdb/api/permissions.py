from rest_framework import permissions


class IsAdminRole(permissions.BasePermission):
    """Только для администраторов."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin)


class IsAdminOrReadOnly(permissions.BasePermission):
    """Администраторы могут всё, остальные только читать."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (request.user.is_authenticated
                and request.user.is_admin)


class IsAuthorOrAdminOrModeratorOrReadOnly(permissions.BasePermission):
    """
    Права для отзывов и комментариев:
    - Читать могут все
    - Изменять может автор, админ, модератор.
    """

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        if not user.is_authenticated:
            return False

        return (
            obj.author == user
            or user.is_admin
            or user.is_moderator
        )
