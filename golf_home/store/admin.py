from django.contrib import admin
from .models import Product, TypeProduct, BrandProduct, ProductPhotos, Review, InfoProduct, Basket, BasketProduct, \
    CategoryProduct, User


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'price', 'time_create')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('photos',)


class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('type', 'brand')


class TypeProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class BrandProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'photo')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('type', 'categories')


class ProductPhotosAdmin(admin.ModelAdmin):
    list_display = ('image',)


admin.site.register(User)

admin.site.register(Product, ProductAdmin)
admin.site.register(CategoryProduct, CategoryProductAdmin)
admin.site.register(TypeProduct, TypeProductAdmin)
admin.site.register(BrandProduct, BrandProductAdmin)

admin.site.register(ProductPhotos, ProductPhotosAdmin)

admin.site.register(Review)
admin.site.register(InfoProduct)
admin.site.register(Basket)
admin.site.register(BasketProduct)
