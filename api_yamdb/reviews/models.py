from django.contrib.auth import get_user_model
from django.db import models

from .constants import MAX_CHAR_FIELD_LENGTH

User = get_user_model()


class Category(models.Model):
    """
    Модель для категорий произведений.
    Категории определяют тип произведения: фильмы, книги, музыка и т.д.
    """
    title = models.CharField(
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
    title = models.CharField(
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
        ordering = ['name']

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """
    Промежуточная таблица для связи многие-ко-многим между Title и Genre.
    Обеспечивает связь между произведениями и жанрами с дополнительной
    возможностью расширения (например, добавить поле порядка сортировки).
    """

    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='genre_titles',
        verbose_name='Жанр'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title_genres',
        verbose_name='Произведение'
    )

    class Meta:
        db_table = 'genre_title'
        constraints = [
            models.UniqueConstraint(
                fields=['genre', 'title'],
                name='unique_genre_title'
            )
        ]
        verbose_name = 'жанр произведения'
        verbose_name_plural = 'Жанры произведения'
        ordering = ['genre']

    def __str__(self):
        return f'{self.title.name}  ({self.genre.title})'
