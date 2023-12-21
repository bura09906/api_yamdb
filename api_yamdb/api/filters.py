from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter

from titles.models import Title


class TitleFilter(FilterSet):
    category = CharFilter(field_name='category__slug', lookup_expr='exact')
    genre = CharFilter(field_name='genre__slug', lookup_expr='exact')
    name = CharFilter(lookup_expr='icontains')
    year = NumberFilter()

    class Meta:
        models = Title
        fields = ('category', 'genre', 'name', 'year')
