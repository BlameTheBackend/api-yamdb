from rest_framework import serializers

from reviews.models import Category, Genre, Title, Review, Comment
from reviews.constants import MIN_RATE, MAX_RATE


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('title', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('title', 'slug')
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('author', 'pub_date', 'title')

    def validate_score(self, rate):
        if not MIN_RATE <= rate <= MAX_RATE:
            raise serializers.ValidationError(
                f'Оценка должна быть от {MIN_RATE} до {MAX_RATE}'
            )
        return rate

    def validate(self, data):
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
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author', 'pub_date', 'review')
