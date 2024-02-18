import django_filters
from .models import Movies


class MovieFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Movies
        fields = ['title', 'genre']