from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from titles.models import Title

User = get_user_model()


class BaseReviewComment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        abstract = True


class Review(BaseReviewComment):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Произведение',
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                settings.MIN_VALUE_SCORE_REVIEW,
                message='Минимальная оценка - 1'
            ),
            MaxValueValidator(
                settings.MAX_VALUE_SCORE_REVIEW,
                message='Максимальная оценка -10'
            ),
        ],
    )

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


class Comment(BaseReviewComment):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Отзыв'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']
