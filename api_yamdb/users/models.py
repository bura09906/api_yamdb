from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import validate_username, username_validator


class UserProfile(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    CHOICES = (
        (USER, 'пользователь'),
        (MODERATOR, 'модератор'),
        (ADMIN, 'админ'),
    )

    username = models.CharField(
        _('username'),
        max_length=settings.LENGTH_USERNAME_FIELDS,
        unique=True,
        help_text=_('Required. 150 characters or fewer.'
                    'Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator, validate_username],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(
        _('email address'),
        max_length=settings.LENGTH_EMAIL_FIELDS,
        unique=True,
        help_text='Поле email обязательно для регистрации'
    )
    bio = models.TextField(
        'Биография',
        blank=True,
        help_text='Биография пользователя'
    )
    role = models.TextField(
        'Роль',
        default='user',
        choices=CHOICES,
        help_text=('Роль пользователя. Допустимые'
                   'значения: user, admin, moderator')
    )

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR or self.is_staff
