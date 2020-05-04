from django_filters import rest_framework as filters
from .models import MainObject


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class MainObjectFilter(filters.FilterSet):
    tag = CharFilterInFilter(field_name='tag__name', lookup_expr='in')
    #date_create = filters.RangeFilter()

    class Meta:
        model = MainObject
        fields = [
            'tag'#, 'date_create'
        ]
