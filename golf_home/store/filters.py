from .models import Product
from django_filters import rest_framework as filters


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ProductFilter(filters.FilterSet):
    # Ищем по слагу, можно задать несколько типов или брэндов
    type = CharFilterInFilter(field_name='type__slug', lookup_expr='in')
    brand = CharFilterInFilter(field_name='brand__slug', lookup_expr='in')
    # Мин. макс. и диапазон цен
    price = filters.RangeFilter()

    class Meta:
        # Наша модель
        model = Product
        fields = ['type', 'brand']
