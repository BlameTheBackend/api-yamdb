from rest_framework import filters, mixins, viewsets, status
from rest_framework.response import Response

from .permissions import IsAdminOrReadOnly


class CreateListDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Базовый вьюсет для моделей, которым нужны только:
    - список (list)
    - создание (create)
    - удаление (destroy)
    GET запрос к конкретному объекту (retrieve) запрещён.
    """
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)

    def retrieve(self, request, *args, **kwargs):
        """Запрещаем получение конкретного объекта."""
        return Response(
            {'detail': 'Method "GET" for single object not allowed.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
