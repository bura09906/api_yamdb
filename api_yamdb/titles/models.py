from django.conf import settings
from django.db import models

from .validators import validate_year


class BaseGenreCategory(models.Model):
    name = models.CharField(
        'Название', unique=True,
        max_length=settings.LENGTH_NAME_FIELDS
    )
    slug = models.SlugField(
        'Идентификатор', unique=True,
        max_length=settings.LENGTH_SLUG_FIELDS
    )

    class Meta:
        abstract = True
        ordering = ['name']


class Genre(BaseGenreCategory):
    pass


class Category(BaseGenreCategory):
    pass


class Title(models.Model):
    name = models.CharField('Название', max_length=settings.LENGTH_NAME_FIELDS)
    year = models.PositiveSmallIntegerField('Год', validators=[validate_year])
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр',
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        verbose_name='Категория', related_name='title',
        null=True
    )
    description = models.CharField(
        'Описание',
        max_length=settings.LENGTH_DESCRIPTION_FIELDS,
        blank=True, null=True
    )
