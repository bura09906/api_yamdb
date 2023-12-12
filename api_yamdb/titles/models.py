from django.core.validators import validate_slug
from django.db import models

from .validators import validate_year


class Genre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(
        'Идентификатор', unique=True, max_length=50, validators=[validate_slug]
    )


class Category(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(
        'Идентификатор', unique=True, max_length=50, validators=[validate_slug]
    )


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.PositiveSmallIntegerField('Год', validators=[validate_year])
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр',
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        verbose_name='Категория', related_name='title',
        null=True
    )
    description = models.CharField(
        'Описание', max_length=200, blank=True, null=True
    )


class GenreTitle(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.genre} {self.title}'
