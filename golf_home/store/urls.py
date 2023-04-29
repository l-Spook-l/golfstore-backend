from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import StoreViewSet, BrandViewSet, TypeViewSet, InfoProductViewSet, BasketViewSet, ReviewViewSet, \
    ProductPhotosViewSet, BasketProductViewSet, CategoryViewSet, ProductListByCategory

product_list = StoreViewSet.as_view({'get': 'list'})
product_detail = StoreViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
# product_detail = StoreViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'})
product_create = StoreViewSet.as_view({'post': 'create'})

urlpatterns = format_suffix_patterns([
    path('product/', product_list),
    path('product/<int:pk>/', product_detail),
    path('product-create/', product_create),

    path('brands/', BrandViewSet.as_view({'get': 'list'})),
    path('brand/<slug:slug>/', BrandViewSet.as_view({'get': 'retrieve'})),

    path('types/', TypeViewSet.as_view({'get': 'list'})),
    path('type/<slug:slug>/', TypeViewSet.as_view({'get': 'retrieve'})),

    path('categories/', CategoryViewSet.as_view({'get': 'list'})),
    path('category-info/<slug:slug>/', CategoryViewSet.as_view({'get': 'retrieve'})),

    path('category/<slug:category_slug>/', ProductListByCategory.as_view({'get': 'list'})),

    path('review/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('review/<int:pk>/', ReviewViewSet.as_view({'put': 'update', 'delete': 'destroy'})),

    path('info-product/',
         InfoProductViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})),
    path('basket/', BasketViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})),
    path('basket-product/',
         BasketProductViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})),
    path('photo-product/',
         ProductPhotosViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'})),
])
