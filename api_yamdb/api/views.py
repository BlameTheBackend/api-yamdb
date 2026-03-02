from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Category, Genre, Title, Review
from users.utils import generate_confirmation_code
from .permissions import (
    IsAdminRole,
    IsAdminOrReadOnly,
    IsAuthorOrAdminOrModeratorOrReadOnly
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer,
    UserSerializer,
    MyselfSerializer,
    SignupSerializer,
    TokenSerializer
)
from .mixins import CreateListDestroyViewSet
from .filters import TitleFilter

User = get_user_model()


class SignupView(APIView):
    """Регистрация нового пользователя и отправка кода подтверждения."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_code = generate_confirmation_code(user)
        send_mail(
            subject='Ваш код подтверждения',
            message=f'Код: {confirmation_code}',
            from_email=None,
            recipient_list=[user.email]
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    """Получение JWT токена по username и коду подтверждения."""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Управление пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = MyselfSerializer(user)
        else:
            serializer = MyselfSerializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data)


class CategoryViewSet(CreateListDestroyViewSet):
    """
    Управление категориями.
    Доступно: список, создание, удаление.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyViewSet):
    """
    Управление жанрами.
    Доступно: список, создание, удаление.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Управление произведениями с рейтингом и фильтрацией."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_class = TitleFilter
    search_fields = ('name', 'description')


class ReviewViewSet(viewsets.ModelViewSet):
    """Управление отзывами на произведения."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrAdminOrModeratorOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['title'] = self.get_title()
        return context


class CommentViewSet(viewsets.ModelViewSet):
    """Управление комментариями к отзывам."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdminOrModeratorOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
