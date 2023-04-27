from rest_framework import serializers
from .models import Product, BrandProduct, TypeProduct, InfoProduct, Basket, BasketProduct, Gender, Review, \
    ProductPhotos, CategoryProduct


class ProductPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhotos
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    # Если надо чтобы присоздании чего либой в модель записывался текущий пользователь
    # user = user в модели если есть (урок 10)
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    username = serializers.StringRelatedField(source='user.username')

    class Meta:
        model = Review
        fields = "__all__"  # если надо все поля


# Сериализатор конвертирует обьекты python (списки, словари...) в JSON
# создание сериализатора
class StoreSerializer(serializers.ModelSerializer):
    # Вместо id получаем названия из полей - name
    type = serializers.SlugRelatedField(slug_field="name", read_only=True)
    brand = serializers.SlugRelatedField(slug_field="name", read_only=True)
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    gender = serializers.SlugRelatedField(slug_field="name", read_only=True)
    photos = ProductPhotosSerializer(many=True)
    reviews = ReviewSerializer(many=True)  # related_name=reviews в модели Review

    class Meta:
        # Подключаем модель из нашей БД
        model = Product
        # Какие поля из модели нам нужно вернуть клиенту (cat_id - ненадо)
        # fields = ('title', 'content', 'cat')
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandProduct
        fields = "__all__"


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeProduct
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)

    class Meta:
        model = CategoryProduct
        fields = "__all__"


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = "__all__"


class InfoProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoProduct
        fields = "__all__"


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = "__all__"


class BasketProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketProduct
        fields = "__all__"
