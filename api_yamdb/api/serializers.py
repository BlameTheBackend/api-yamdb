import re

from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import NotFound

from reviews.constants import MIN_RATE, MAX_RATE
from reviews.models import Category, Genre, Title, Review, Comment
from users.utils import check_confirmation_code


User = get_user_model()


class SignupSerializer(serializers.Serializer):
    """Регистрация новых пользователей."""

    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)

    def validate_username(self, value):
        """Проверка username: не 'me' и только допустимые символы."""

        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" запрещено для регистрации'
            )

        if not re.match(r'^[\w.@+-]+$', value):
            raise serializers.ValidationError(
                'Username может содержать только буквы,'
                'цифры и символы @/./+/-/_'
            )
        return value

    def validate_email(self, value):
        """Проверка длины email (макс. 254)."""

        if len(value) > 254:
            raise serializers.ValidationError(
                'Email не может быть длиннее 254 символов'
            )
        return value

    def validate(self, data):
        """Проверка уникальности username и email."""

        username = data.get('username')
        email = data.get('email')

        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.email != email:
                raise serializers.ValidationError(
                    'Пользователь с таким username уже существует'
                )

        if (
            User.objects.filter(email=email)
            .exclude(username=username)
            .exists()
        ):
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует'
            )

        return data

    def create(self, validated_data):
        """Создание или получение пользователя."""

        user, created = User.objects.get_or_create(
            username=validated_data['username'],
            defaults={'email': validated_data['email']}
        )
        return user


class TokenSerializer(serializers.Serializer):
    """Получение JWT токена по username и коду подтверждения."""

    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        """Проверка username и кода подтверждения."""

        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise NotFound('Пользователь не найден')  # DRF сам вернет 404

        if not check_confirmation_code(user, data['confirmation_code']):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный код подтверждения'}
            )

        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User


class MyselfSerializer(serializers.ModelSerializer):
    """Сериализатор для профиля текущего пользователя."""

    role = serializers.CharField(read_only=True)

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для жанров."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для произведений с рейтингом."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating',
            'description', 'category', 'genre'
        )
        model = Title

    def to_representation(self, instance):
        """Замена slug'ов на полные объекты при чтении."""
        rep = super().to_representation(instance)
        rep['category'] = CategorySerializer(instance.category).data
        rep['genre'] = GenreSerializer(instance.genre.all(), many=True).data
        return rep


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author', 'pub_date', 'title')

    def validate_score(self, rate):
        """Проверка оценки (1-10)."""

        if not MIN_RATE <= rate <= MAX_RATE:
            raise serializers.ValidationError(
                f'Оценка должна быть от {MIN_RATE} до {MAX_RATE}'
            )
        return rate

    def validate(self, data):
        """Проверка уникальности отзыва пользователя на произведение."""

        request = self.context['request']
        title = self.context.get('title')

        if request.method == 'POST' and title:
            if Review.objects.filter(
                title=title, author=request.user
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли отзыв на это произведение'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""

    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author', 'pub_date', 'review')
