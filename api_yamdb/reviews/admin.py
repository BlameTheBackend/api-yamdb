from django.contrib import admin
from django.db.models import Avg

from .constants import SHORT_TEXT
from .models import Category, Genre, Title, Review, Comment
from users.models import User


class ShortTextMixin:
    """Миксин для обрезки длинного текста."""

    def short_text(self, obj):
        """Обрезать длинный текст до SHORT_TEXT_LENGTH символов."""
        return (
            obj.text[:SHORT_TEXT] + '…'
            if len(obj.text) > SHORT_TEXT
            else obj.text
        )
    short_text.short_description = 'Текст'


class BaseNameSlugAdmin(admin.ModelAdmin):
    """Базовый класс для админки моделей с name и slug."""
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Category)
class CategoryAdmin(BaseNameSlugAdmin):
    """Категории произведений."""
    pass


@admin.register(Genre)
class GenreAdmin(BaseNameSlugAdmin):
    """Жанры произведений."""
    pass


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Произведения."""
    list_display = (
        'id', 'name', 'year', 'category', 'display_genres', 'rating'
    )
    list_filter = ('year', 'category', 'genre')
    search_fields = ('name', 'description')
    filter_horizontal = ('genre',)
    raw_id_fields = ('category',)
    ordering = ('-year', 'name')

    def get_queryset(self, request):
        """Аннотация рейтинга."""
        return super().get_queryset(request).annotate(
            rating_avg=Avg('reviews__score')
        )

    def display_genres(self, obj):
        """Жанры через запятую (первые 3)."""
        genre_names = obj.genre.values_list('name', flat=True)[:3]
        return ', '.join(genre_names)
    display_genres.short_description = 'Жанры'

    def rating(self, obj):
        """Средняя оценка из аннотированного поля."""
        if hasattr(obj, 'rating_avg') and obj.rating_avg:
            return round(obj.rating_avg, 1)
        return '—'
    rating.short_description = 'Рейтинг'


@admin.register(Review)
class ReviewAdmin(ShortTextMixin, admin.ModelAdmin):
    """Отзывы."""
    list_display = (
        'id', 'title_name', 'author', 'score', 'pub_date', 'short_text'
    )
    list_filter = ('score', 'pub_date')
    search_fields = ('text', 'author__username', 'title__name')
    raw_id_fields = ('author', 'title')
    ordering = ('-pub_date',)

    def title_name(self, obj):
        return obj.title.name

    title_name.short_description = 'Произведение'
    title_name.admin_order_field = 'title__name'


@admin.register(Comment)
class CommentAdmin(ShortTextMixin, admin.ModelAdmin):
    """Комментарии."""
    list_display = ('id', 'review_info', 'author', 'pub_date', 'short_text')
    list_filter = ('pub_date',)
    search_fields = ('text', 'author__username')
    raw_id_fields = ('author', 'review')
    ordering = ('-pub_date',)

    def review_info(self, obj):
        return f'Отзыв #{obj.review.id} на "{obj.review.title.name}"'

    review_info.short_description = 'Отзыв'
    review_info.admin_order_field = 'review'


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Пользователи."""
    list_display = (
        'id', 'username', 'email', 'role', 'is_active', 'date_joined'
    )
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email')
    ordering = ('-date_joined',)
    fieldsets = (
        ('Основное', {
            'fields': ('username', 'email', 'password')
        }),
        ('Личная информация', {
            'fields': ('bio',)
        }),
        ('Права', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser')
        }),
    )
