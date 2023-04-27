from .models import Product
from django_filters import rest_framework as filters


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class ProductFilter(filters.FilterSet):
    # Ищем по слагу, можно задать несколько типов или брэндов
    type = CharFilterInFilter(field_name='type__slug', lookup_expr='in')
    brand = CharFilterInFilter(field_name='brand__slug', lookup_expr='in')
    category = CharFilterInFilter(field_name='category__slug', lookup_expr='in')
    gender = CharFilterInFilter(field_name='gender__slug', lookup_expr='in')

    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")

    ordering = filters.OrderingFilter(fields=["time_create", "price"])

    class Meta:
        model = Product
        fields = ['type', 'brand', 'gender', 'category', 'min_price', 'max_price']
