from django.db import models

from .constants import MAX_CHAR_FIELD_LENGTH
from .validators import validate_year, validate_score
from .abstract_models import ContentModel, NameSlugModel


class Category(NameSlugModel):
    """
    Модель для категорий произведений.
    Категории определяют тип произведения: фильмы, книги, музыка и т.д.
    """

    class Meta(NameSlugModel.Meta):
        db_table = 'category'
        verbose_name = 'Категория'
        verbose_name_plural = 'категории'


class Genre(NameSlugModel):
    """
    Модель для жанров произведений.
    Жанры определяют стиль или направление произведения:
    драма, комедия, рок и т.д.
    """

    class Meta(NameSlugModel.Meta):
        db_table = 'genre'
        verbose_name = 'Жанр'
        verbose_name_plural = 'жанры'


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
        verbose_name='Год выпуска',
        validators=[validate_year]
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


class Review(ContentModel):
    """
    Модель для отзывов на произведения.
    """
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение'
    )
    score = models.IntegerField(
        validators=[validate_score],
        verbose_name='Оценка'
    )

    class Meta(ContentModel.Meta):
        db_table = 'review'
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return f'Отзыв {self.author} на {self.title}'


class Comment(ContentModel):
    """
    Модель для комментариев к отзывам.
    """
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий'
    )

    class Meta(ContentModel.Meta):
        db_table = 'comment'
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий {self.author} к отзыву {self.review.id}'
