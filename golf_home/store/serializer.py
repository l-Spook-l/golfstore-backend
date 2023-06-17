from .models import User

from rest_framework import serializers
from .models import Product, BrandProduct, TypeProduct, InfoProduct, Basket, BasketProduct, WishList, WishListProduct, \
    Gender, Review, ProductPhotos, CategoryProduct


class ProductPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPhotos
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    first_name = serializers.StringRelatedField(source='user.first_name')

    class Meta:
        model = Review
        fields = "__all__"  # если надо все поля


class InfoProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoProduct
        fields = "__all__"


class StoreSerializer(serializers.ModelSerializer):
    # Вместо id получаем названия из полей - name
    type = serializers.SlugRelatedField(slug_field="name", read_only=True)
    brand = serializers.SlugRelatedField(slug_field="name", read_only=True)
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    gender = serializers.SlugRelatedField(slug_field="name", read_only=True)
    photos = ProductPhotosSerializer(many=True)
    reviews = ReviewSerializer(many=True)  # related_name=reviews в модели Review
    options = InfoProductSerializer(many=True)

    class Meta:
        model = Product
        fields = "__all__"


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeProduct
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandProduct
        fields = ('id', 'name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryProduct
        fields = ('id', 'name', 'slug')


class BrandWithTypeAndCategorySerializer(serializers.ModelSerializer):
    type = TypeSerializer(many=True)
    categories = CategorySerializer(many=True)

    class Meta:
        model = BrandProduct
        fields = "__all__"


class CategoryWithTypeAndBrandSerializer(serializers.ModelSerializer):
    type = TypeSerializer(many=True)
    brand = BrandSerializer(many=True)

    class Meta:
        model = CategoryProduct
        fields = "__all__"


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = "__all__"


class BasketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basket
        fields = "__all__"


class BasketProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketProduct
        fields = "__all__"


class ProductForBasketSerializer(serializers.ModelSerializer):
    photos = ProductPhotosSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'photos')


class ProductListByBasketSerializer(serializers.ModelSerializer):
    product = ProductForBasketSerializer()

    class Meta:
        model = BasketProduct
        fields = "__all__"


class WishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = "__all__"


class WishListProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishListProduct
        fields = "__all__"


class ProductForWishListSerializer(serializers.ModelSerializer):
    photos = ProductPhotosSerializer(many=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'photos')


class ProductListByWishListSerializer(serializers.ModelSerializer):
    product = ProductForWishListSerializer()

    class Meta:
        model = WishListProduct
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone_number', 'card_number')
