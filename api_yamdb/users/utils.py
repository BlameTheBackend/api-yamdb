from django.contrib.auth.tokens import default_token_generator


def generate_confirmation_code(user):
    """Генерирует код подтверждения для пользователя."""
    return default_token_generator.make_token(user)


def check_confirmation_code(user, code):
    """Проверяет код подтверждения пользователя."""
    return default_token_generator.check_token(user, code)
