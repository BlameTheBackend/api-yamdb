from django.contrib.auth.tokens import default_token_generator


def generate_confirmation_code(user):
    return default_token_generator.make_token(user)


def check_confirmation_code(user, code):
    return default_token_generator.check_token(user, code)
