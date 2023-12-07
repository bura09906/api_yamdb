from django.db import models
from django.db.models import Avg
from django.core.validators import validate_slug
from .validators import validate_year
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
User = get_user_model()


class Genre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Идентификатор',
                            unique=True, max_length=50,
                            validators=[validate_slug])


class Category(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Идентификатор', unique=True, max_length=50,
                            validators=[validate_slug])


class Title(models.Model):
    name = models.CharField(
        'Название', max_length=256
    )
    year = models.PositiveSmallIntegerField(
        'Год', validators=[validate_year]
    )
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр',
        through='GenreTitle'
    )
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING,
        verbose_name='Категория', related_name='title',
        unique=False
    )
    description = models.CharField('Описание',
                                   max_length=200,
                                   blank=True, null=True)

    @property
    def rating(self):
        if hasattr(self, '_average_rating'):
            return self._average_rating
        return self.reviews.aggregate(Avg("score"))['score__avg']


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.DO_NOTHING)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Произведение',
    )
    text = models.TextField(verbose_name='Текст', unique=True)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        validators=[
            MinValueValidator(1, message='Минимальная оценка - 1'),
            MaxValueValidator(10, message='Максимальная оценка -10'),
        ],
    )
    rating = models.ForeignKey(Title, on_delete=models.CASCADE,
                               verbose_name='Рейтинг',
                               related_name='rating',
                               blank=True,
                               null=True)

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                name='unique_author_title',
                fields=['author', 'title'],
            ),
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']
