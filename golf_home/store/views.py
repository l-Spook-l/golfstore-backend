from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from .filters import ProductFilter, CategoryFilter, BrandFilter
from .models import Product, TypeProduct, BrandProduct, InfoProduct, Basket, BasketProduct, WishList, WishListProduct, \
    Gender, Review, ProductPhotos, CategoryProduct, User
from .serializer import StoreSerializer, BrandWithTypeAndCategorySerializer, TypeSerializer, InfoProductSerializer, \
    BasketSerializer, ReviewSerializer, ProductPhotosSerializer, BasketProductSerializer, GenderSerializer, \
    WishListSerializer, WishListProductSerializer, CategoryWithTypeAndBrandSerializer, ProductListByBasketSerializer, \
    ProductListByWishListSerializer, UserSerializer


class ProductAPILIstPagination(PageNumberPagination):
    page_size = 24  # кол-во записей на 1й стр
    page_query_param = 'page'
    max_page_size = 1000  # Ограничение записей на 1й стр для - page_query_param = 'page_size'


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()  # Берем все записи из нужной табл в БД
    serializer_class = StoreSerializer  # подключаем DRF
    filterset_class = ProductFilter  # фильтрации записей модели "Product" на основе параметров запроса
    filter_backends = [DjangoFilterBackend]
    pagination_class = ProductAPILIstPagination  # Пагинация
    lookup_field = 'slug'


class ProductPhotosViewSet(viewsets.ModelViewSet):
    queryset = ProductPhotos.objects.all()
    serializer_class = ProductPhotosSerializer


class TypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TypeProduct.objects.all()
    serializer_class = TypeSerializer
    lookup_field = 'slug'


class BrandViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BrandProduct.objects.all()
    serializer_class = BrandWithTypeAndCategorySerializer
    lookup_field = 'slug'  # обращаемся по slug вместо id


class ProductListByBrand(viewsets.ReadOnlyModelViewSet):
    serializer_class = StoreSerializer
    filterset_class = BrandFilter
    filter_backends = [DjangoFilterBackend]
    pagination_class = ProductAPILIstPagination

    def get_queryset(self):
        brand_slug = self.kwargs['brand_slug']
        brand = get_object_or_404(BrandProduct, slug=brand_slug)
        queryset = Product.objects.filter(brand=brand)
        return queryset


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CategoryProduct.objects.all()
    serializer_class = CategoryWithTypeAndBrandSerializer
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
    lookup_field = 'user'

    def get_queryset(self):
        user = self.kwargs['user']
        queryset = Basket.objects.filter(user=user)
        return queryset


class AddProductToBasketViewSet(viewsets.ModelViewSet):
    queryset = BasketProduct.objects.all()
    serializer_class = BasketProductSerializer


class BasketProductViewSet(viewsets.ModelViewSet):
    queryset = BasketProduct.objects.all()
    serializer_class = ProductListByBasketSerializer
    lookup_field = 'product_id'

    def get_queryset(self):
        basket_id = self.kwargs['basket_id']
        basket = get_object_or_404(Basket, id=basket_id)
        queryset = BasketProduct.objects.filter(basket=basket)
        return queryset


class WishListViewSet(viewsets.ModelViewSet):
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    lookup_field = 'user'

    def get_queryset(self):
        user = self.kwargs['user']
        queryset = WishList.objects.filter(user=user)
        return queryset


class AddProductToWishListViewSet(viewsets.ModelViewSet):
    queryset = WishListProduct.objects.all()
    serializer_class = WishListProductSerializer


class WishListProductViewSet(viewsets.ModelViewSet):
    queryset = WishListProduct.objects.all()
    serializer_class = ProductListByWishListSerializer
    lookup_field = 'product_id'

    def get_queryset(self):
        wishlist_id = self.kwargs['wishlist_id']
        wishlist = get_object_or_404(WishList, id=wishlist_id)
        queryset = WishListProduct.objects.filter(wishlist=wishlist)
        return queryset


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]


class UserInfoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
