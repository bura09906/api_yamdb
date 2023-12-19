from django.core.exceptions import ValidationError
from django.contrib.auth.validators import UnicodeUsernameValidator


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            'Имя пользователя me недопустимо'
        )


username_validator = UnicodeUsernameValidator()
