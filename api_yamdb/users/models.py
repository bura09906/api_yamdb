from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

CHOICES = (
    ('user', 'пользователь'),
    ('moderator', 'модератор'),
    ('admin', 'админ'),
)


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), null=False, unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.TextField('Роль', default='user', choices=CHOICES)


class ConfirmationCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=12)
    date = models.DateTimeField(auto_now=True)
