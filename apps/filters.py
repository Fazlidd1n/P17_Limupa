import django_filters

from apps.models import Blog


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Blog
        fields = ('name',)
