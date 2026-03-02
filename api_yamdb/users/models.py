from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'user'
        MODERATOR = 'moderator'
        ADMIN = 'admin'

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Email'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.USER,
        verbose_name='Роль'
    )

    REQUIRED_FIELDS = ['email']

    @property
    def is_admin(self):
        """Проверка, является ли пользователь администратором."""
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        """Проверка, является ли пользователь модератором."""
        return self.role == self.Role.MODERATOR

    @property
    def is_user(self):
        """Проверка, является ли пользователь обычным пользователем."""
        return self.role == self.Role.USER

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __str__(self):
        return self.username
