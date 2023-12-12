from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter


class TitleFilter(FilterSet):
    category = CharFilter(field_name='category__slug', lookup_expr='exact')
    genre = CharFilter(field_name='genre__slug', lookup_expr='exact')
    name = CharFilter(lookup_expr='icontains')
    year = NumberFilter()
