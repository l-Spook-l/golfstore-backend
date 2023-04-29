from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.pagination import PageNumberPagination

from .filters import ProductFilter, CategoryFilter
from .models import Product, TypeProduct, BrandProduct, InfoProduct, Basket, BasketProduct, Gender, Review, \
    ProductPhotos, CategoryProduct
from .serializer import StoreSerializer, BrandSerializer, TypeSerializer, InfoProductSerializer, BasketSerializer, \
    ReviewSerializer, ProductPhotosSerializer, BasketProductSerializer, GenderSerializer, CategorySerializer


class ProductAPILIstPagination(PageNumberPagination):
    page_size = 25  # кол-во записей на 1й стр
    # 'page_size' - доп. пар-р в get запросе (нарп. можно получать больше или меньше записей page_size=20)
    page_query_param = 'page'
    max_page_size = 1000  # Ограничение записей на 1й стр для - page_query_param = 'page_size'


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()  # Берем все записи из нужной табл в БД
    serializer_class = StoreSerializer  # подключаем DRF
    filterset_class = ProductFilter  # фильтрации записей модели "Product" на основе параметров запроса
    filter_backends = [DjangoFilterBackend]
    pagination_class = ProductAPILIstPagination  # Пагинация

    # Параметры доступа
    # def get_permissions(self):
    #     if self.action == 'list' or self.action == 'retrieve':
    #         # if self.action == 'list':
    #         permission_classes = [permissions.AllowAny]
    #     else:
    #         permission_classes = [permissions.IsAdminUser]
    #     return [permission() for permission in permission_classes]


class ProductPhotosViewSet(viewsets.ModelViewSet):
    queryset = ProductPhotos.objects.all()
    serializer_class = ProductPhotosSerializer


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BrandProduct.objects.all()
    serializer_class = BrandSerializer
    lookup_field = 'slug'  # обращаемся по slug вместо id


class TypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TypeProduct.objects.all()
    serializer_class = TypeSerializer
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CategoryProduct.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'


class ProductListByCategory(viewsets.ReadOnlyModelViewSet):
    serializer_class = StoreSerializer
    filterset_class = CategoryFilter
    filter_backends = [DjangoFilterBackend]
    pagination_class = ProductAPILIstPagination

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        category = get_object_or_404(CategoryProduct, slug=category_slug)
        queryset = Product.objects.filter(category=category)
        return queryset


class GenderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer
    lookup_field = 'slug'


class InfoProductViewSet(viewsets.ModelViewSet):
    queryset = InfoProduct.objects.all()
    serializer_class = InfoProductSerializer


class BasketViewSet(viewsets.ModelViewSet):
    queryset = Basket.objects.all()
    serializer_class = BasketSerializer


class BasketProductViewSet(viewsets.ModelViewSet):
    queryset = BasketProduct.objects.all()
    serializer_class = BasketProductSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
