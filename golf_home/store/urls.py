from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import StoreViewSet, BrandViewSet, TypeViewSet, InfoProductViewSet, BasketViewSet, ReviewViewSet, \
    ProductPhotosViewSet, AddProductToBasketViewSet, BasketProductViewSet, CategoryViewSet, ProductListByCategory, \
    ProductListByBrand, WishListViewSet, WishListProductViewSet, AddProductToWishListViewSet, UserInfoViewSet

product_list = StoreViewSet.as_view({'get': 'list'})
product_detail = StoreViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
product_create = StoreViewSet.as_view({'post': 'create'})

urlpatterns = format_suffix_patterns([
    path('product/', product_list),
    path('product/<slug:slug>/', product_detail),
    path('product-create/', product_create),

    path('types/', TypeViewSet.as_view({'get': 'list'})),
    path('type/<slug:slug>/', TypeViewSet.as_view({'get': 'retrieve'})),

    path('brands/', BrandViewSet.as_view({'get': 'list'})),
    path('brand-info/<slug:slug>/', BrandViewSet.as_view({'get': 'retrieve'})),
    path('brand/<slug:brand_slug>/', ProductListByBrand.as_view({'get': 'list'})),

    path('categories/', CategoryViewSet.as_view({'get': 'list'})),
    path('category-info/<slug:slug>/', CategoryViewSet.as_view({'get': 'retrieve'})),
    path('category/<slug:category_slug>/', ProductListByCategory.as_view({'get': 'list'})),

    path('review/', ReviewViewSet.as_view({'post': 'create'})),
    path('review/<int:pk>/', ReviewViewSet.as_view({'patch': 'partial_update', 'delete': 'destroy'})),

    path('info-product/',
         InfoProductViewSet.as_view({'post': 'create', 'put': 'update', 'delete': 'destroy'})),

    path('basket/', BasketViewSet.as_view({'post': 'create'})),
    path('basket/<int:user>/', BasketViewSet.as_view({'get': 'retrieve'})),

    path('basket-product/', AddProductToBasketViewSet.as_view({'post': 'create'})),
    path('basket-product/<int:basket_id>/', BasketProductViewSet.as_view({'get': 'list', 'put': 'update'})),
    path('basket-product/<int:basket_id>/<int:product_id>', BasketProductViewSet.as_view({'get': 'retrieve' ,'patch': 'partial_update', 'delete': 'destroy'})),

    path('wishlist/', WishListViewSet.as_view({'post': 'create'})),
    path('wishlist/<int:user>/', WishListViewSet.as_view({'get': 'retrieve'})),

    path('wishlist-product/', AddProductToWishListViewSet.as_view({'post': 'create'})),
    path('wishlist-product/<int:wishlist_id>/', WishListProductViewSet.as_view({'get': 'list'})),
    path('wishlist-product/<int:wishlist_id>/<int:product_id>', WishListProductViewSet.as_view({'delete': 'destroy'})),

    path('user-info/', UserInfoViewSet.as_view({'get': 'list', 'put': 'update'})),

    path('photo-product/', ProductPhotosViewSet.as_view({'post': 'create', 'put': 'update', 'delete': 'destroy'})),
])
