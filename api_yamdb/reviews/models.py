from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .constants import (
    MAX_CHAR_FIELD_LENGTH,
    MAX_RATE,
    MIN_RATE
)

User = get_user_model()


class Category(models.Model):
    """
    Модель для категорий произведений.
    Категории определяют тип произведения: фильмы, книги, музыка и т.д.
    """
    name = models.CharField(
        max_length=MAX_CHAR_FIELD_LENGTH,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Уникальный идентификатор'
    )

    class Meta:
        db_table = 'category'
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.title


class Genre(models.Model):
    """
    Модель для жанров произведений.
    Жанры определяют стиль или направление произведения:
    драма, комедия, рок и т.д.
    """
    name = models.CharField(
        max_length=MAX_CHAR_FIELD_LENGTH,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Уникальный идентификатор'
    )

    class Meta:
        db_table = 'genre'
        verbose_name = 'Жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.title


class Title(models.Model):
    """
    Модель для произведений.
    Хранит информацию о произведении: название, год выпуска,
    категорию и жанры. Связана с моделями Category и Genre.
    """
    name = models.CharField(
        max_length=MAX_CHAR_FIELD_LENGTH,
        verbose_name='Название произведения'
    )
    year = models.IntegerField(
        verbose_name='Год выпуска'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Описание произведения'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True,
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        blank=True,
        verbose_name='Жанры'
    )

    class Meta:
        db_table = 'titles'
        constraints = [
            models.UniqueConstraint(
                fields=['category', 'name'],
                name='unique_category_title'
            )
        ]
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    Модель для отзывов на произведения.
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(MIN_RATE),
            MaxValueValidator(MAX_RATE)
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        db_table = 'review'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return f'Отзыв {self.author} на {self.title}'


class Comment(models.Model):
    """
    Модель для комментариев к отзывам.
    """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий'
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        db_table = 'comment'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'Комментарий {self.author} к отзыву {self.review.id}'
