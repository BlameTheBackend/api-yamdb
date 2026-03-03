from datetime import date

from django.core.exceptions import ValidationError

from .constants import MIN_RATE, MAX_RATE, MIN_YEAR


def validate_year(value):
    """
    Валидатор для проверки года выпуска произведения.
    Год не может быть меньше 1800 и больше текущего года.
    """
    current_year = date.today().year

    if value < MIN_YEAR:
        raise ValidationError(
            f'Год выпуска не может быть меньше {MIN_YEAR}'
        )

    if value > current_year:
        raise ValidationError(
            f'Год выпуска не может быть больше {current_year}'
        )


def validate_score(value):
    """
    Валидатор для проверки оценки.
    Оценка должна быть в пределах от MIN_RATE до MAX_RATE.
    """
    if value < MIN_RATE or value > MAX_RATE:
        raise ValidationError(
            f'Оценка должна быть от {MIN_RATE} до {MAX_RATE}'
        )
