from django.shortcuts import render
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from .serializers import TitleSerializer, GenreSerializer, CategorySerializer
from titles.models import Title, Genre, Category, GenreTitle


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('slug',)


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ('slug',)


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')
    pagination_class = PageNumberPagination

    # def perform_create(self, serializer):
    #     genres = serializer.validated_data.pop('genre')
    #     title = Title.objects.create(**serializer.validated_data)
    #     for genre in genres:
    #         current_genre = get_object_or_404(Genre, slug=genre)
    #         GenreTitle.objects.create(
    #             genre=current_genre, title=title
    #         )
    #     return title
