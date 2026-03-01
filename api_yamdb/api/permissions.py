from rest_framework import permissions


class BasePermission(permissions.BasePermission):
    """Базовый класс с общими методами"""

    def _is_admin(self, user):
        """Проверка, является ли пользователь администратором"""
        return user.is_authenticated and (
            user.role == 'admin' or user.is_staff
        )


class IsAdminRole(BasePermission):
    """Только для администраторов"""

    def has_permission(self, request, view):
        return self._is_admin(request.user)


class IsAdminOrReadOnly(BasePermission):
    """Администраторы могут всё, остальные только читать"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return self._is_admin(request.user)


class IsAuthorOrAdminOrModeratorOrReadOnly(BasePermission):
    """
    Права для отзывов и комментариев:
    - Читать могут все
    - Изменять может автор, админ, модератор
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
            or self._is_admin(user)
            or user.role == 'moderator'
        )
