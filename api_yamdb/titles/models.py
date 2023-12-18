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


class Genre(BaseGenreCategory):
    pass


class Category(BaseGenreCategory):
    pass


class Title(models.Model):
    name = models.CharField('Название', max_length=settings.LENGTH_NAME_FIELDS)
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
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.genre} {self.title}'
