from django.db import models

from .constants import MAX_CHAR_FIELD_LENGTH, MAX_CHAR_SLUG_LENGTH
from users.models import User


class NameSlugModel(models.Model):
    """
    Абстрактная модель для объектов с именем и slug.
    """
    name = models.CharField(
        max_length=MAX_CHAR_FIELD_LENGTH,
        verbose_name='Название'
    )
    slug = models.SlugField(
        max_length=MAX_CHAR_SLUG_LENGTH,
        unique=True,
        verbose_name='Уникальный идентификатор'
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name


class ContentModel(models.Model):
    """
    Абстрактная модель для контента (отзывы и комментарии).
    Содержит текст, автора и дату публикации.
    """
    text = models.TextField(
        verbose_name='Текст'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.__class__.__name__} {self.author} {self.pub_date}'
