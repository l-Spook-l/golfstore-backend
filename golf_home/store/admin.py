from django.contrib import admin
from .models import Product, TypeProduct, BrandProduct, ProductPhotos, Review, InfoProduct, Basket, BasketProduct, \
    CategoryProduct, User

"""
is_superuser - просмотр инфо в админ-панели
is_staff - доступ к админ-панели
"""


# название как правило соападает с нужной моделью
class ProductAdmin(admin.ModelAdmin):
    # список полей которые мы хотим видеть в админ-панеле
    # list_display = ('id', 'name', 'time_create', 'photo', 'is_published')
    list_display = ('id', 'name', 'slug', 'price', 'time_create')
    # клик по этим поляем позволяет перейти на нужную статью
    list_display_links = ('id', 'name')
    # делаем поле редактируемым
    # list_editable = ('is_published',)
    # поля по которым можно будет делать фильтрацию (появляется фильтр справа)
    # list_filter = ('is_published', 'time_create')
    # по каким полям делать поиск
    search_fields = ('name',)
    # автозаполнение слага на основе имени
    prepopulated_fields = {'slug': ('name',)}
    # Если поле manyTOmany
    filter_horizontal = ('photos',)


class CategoryProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    # делаем поле редактируемым
    # list_editable = ('is_published',)
    # поля по которым можно будет делать фильтрацию (появляется фильтр справа)
    # list_filter = ('is_published', 'time_create')
    # по каким полям делать поиск
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    # Если поле manyTOmany
    filter_horizontal = ('type', 'brand')


class TypeProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    # делаем поле редактируемым
    # list_editable = ('is_published',)
    # поля по которым можно будет делать фильтрацию (появляется фильтр справа)
    # list_filter = ('is_published', 'time_create')
    # по каким полям делать поиск
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class BrandProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'photo')
    # клик по этим поляем позволяет перейти на нужную статью
    list_display_links = ('id', 'name')
    # делаем поле редактируемым
    # list_editable = ('is_published',)
    # поля по которым можно будет делать фильтрацию (появляется фильтр справа)
    # list_filter = ('is_published', 'time_create')
    # по каким полям делать поиск
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    # Если поле manyTOmany
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
