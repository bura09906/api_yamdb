from rest_framework import viewsets
from reviews.models import Comment, Review
from titles.models import Title
from api.serializers import (
    CommentSerializer, ReviewSerializer
)
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from .permissions import IsAuthorOrReadOnly


class TitleViewSet(viewsets.ModelViewSet):
    queryset = (Title.objects
                .annotate(rating=Avg("reviews__score")).all()
                .order_by("name")
                )


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())
