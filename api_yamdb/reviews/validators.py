from datetime import date

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .constants import MIN_RATE, MAX_RATE


def validate_year(value):
    """
    Валидатор для проверки года выпуска произведения.
    Год не может быть меньше 1800 и больше текущего года.
    """
    current_year = date.today().year

    if value < 1800:
        raise ValidationError(
            _('Год выпуска не может быть меньше %(min_year)s'),
            params={'min_year': 1800},
        )

    if value > current_year:
        raise ValidationError(
            _('Год выпуска не может быть больше %(current_year)s'),
            params={'current_year': current_year},
        )


def validate_score(value):
    """
    Валидатор для проверки оценки.
    Оценка должна быть в пределах от MIN_RATE до MAX_RATE.
    """
    if value < MIN_RATE or value > MAX_RATE:
        raise ValidationError(
            _(f'Оценка должна быть от {MIN_RATE} до {MAX_RATE}'),
            params={
                'min_rate': MIN_RATE,
                'max_rate': MAX_RATE,
                'value': value
            },
        )
