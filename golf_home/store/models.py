from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import models as auth_models


class UserManager(auth_models.BaseUserManager):
    def create_user(self, first_name: str, last_name: str, email: str, password: str = None, is_staff=False,
                    is_superuser=False) -> "User":
        if not email:
            raise ValueError("User must have an email")
        if not first_name:
            raise ValueError("User must have a first_name")
        if not last_name:
            raise ValueError("User must have a last_name")

        user = self.model(email=self.normalize_email(email))
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.is_active = True
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save()

        return user

    def create_superuser(self, first_name: str, last_name: str, email: str, password: str) -> "User":
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True,
        )
        user.save()

        return user


class User(auth_models.AbstractUser):
    first_name = models.CharField(verbose_name="First name", max_length=255)
    last_name = models.CharField(verbose_name="Last name", max_length=255)
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.first_name


class TypeProduct(models.Model):
    """Тип продукта, первичная модель"""
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    # для настройки в админ-панели
    class Meta:
        verbose_name = 'Тип продукта'
        verbose_name_plural = 'Типы продуктов'
        ordering = ['name']  # сортировка везде

    def get_absolute_url(self):
        # type -  название в URL (name='type')
        return reverse('type', kwargs={'type_slug': self.slug})


class BrandProduct(models.Model):
    """Производитель продукта, первичная модель"""
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    photo = models.ImageField(upload_to='photos/brand/', blank=True)
    description = models.TextField(max_length=5000)
    type = models.ManyToManyField(TypeProduct, blank=True)
    categories = models.ManyToManyField('CategoryProduct', blank=True)

    def __str__(self):
        return self.name

    # для настройки в админ-панели
    class Meta:
        verbose_name = 'Брэнд продукта'
        verbose_name_plural = 'Брэнды продуктов'
        ordering = ['name']  # сортировка везде

    def get_absolute_url(self):
        # brand - название в URL (name='brand')
        return reverse('brand', kwargs={'brand_slug': self.slug})


class CategoryProduct(models.Model):
    """Категория продукта, первичная модель"""
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    type = models.ManyToManyField(TypeProduct, blank=True)
    brand = models.ManyToManyField(BrandProduct, blank=True)

    def __str__(self):
        return self.name

    # для настройки в админ-панели
    class Meta:
        verbose_name = 'Категория продукта'
        verbose_name_plural = 'Категории продуктов'
        ordering = ['name']  # сортировка везде

    def get_absolute_url(self):
        # category - название в URL (name='category')
        return reverse('category', kwargs={'category_slug': self.slug})


class ProductPhotos(models.Model):
    image = models.ImageField(upload_to='photos/product')

    def __str__(self):
        return self.image.name

    # для настройки в админ-панели
    class Meta:
        verbose_name = 'Фото продукта'
        verbose_name_plural = 'Фотографии продуктов'


class Gender(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('gender', kwargs={'gender_slug': self.slug})


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    price = models.IntegerField()
    photos = models.ManyToManyField(ProductPhotos, blank=True)
    category = models.ForeignKey(CategoryProduct, on_delete=models.PROTECT)
    type = models.ForeignKey(TypeProduct, on_delete=models.PROTECT, blank=True)
    brand = models.ForeignKey(BrandProduct, on_delete=models.PROTECT, blank=True)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT, blank=True)
    time_create = models.DateTimeField(auto_now_add=True)  # принимаем текущее время и не меняется

    def __str__(self):
        return self.name

    # метод для получения нужного - url, так же при использовании классов, помогает перенаправить на нужную стр.
    # помогает в админ-панели сгенерировать кнопку (смотреть на сайте)
    def get_absolute_url(self):
        return reverse('product', kwargs={'product_slug': self.slug})

    # авто формирование слага
    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    # при удалении продукта, удалять из папки фото
    def delete(self, *args, **kwargs):
        # Удаляем файл, связанный с этой записью
        self.photos.delete()
        super().delete(*args, **kwargs)

    # для настройки в админ-панели
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['time_create', 'price', '-price']  # сортировка везде


class InfoProduct(models.Model):
    title = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='options')
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class BasketProduct(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class WishList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class WishListProduct(models.Model):
    wishlist = models.ForeignKey(WishList, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


class Review(models.Model):
    """Модель отзывов для продукта"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    comment = models.TextField(max_length=5000)
    parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name

    class Meta:
        ordering = ['created_at']
