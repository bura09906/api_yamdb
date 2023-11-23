from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


CHOICES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'админ'),
)


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), null=False)
    bio = models.TextField('Биография', blank=True)
    role = models.TextField('Роль', default='user', choices=CHOICES)
