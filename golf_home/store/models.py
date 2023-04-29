from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User


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
        # category -  название в URL (name='category')
        return reverse('category', kwargs={'category_slug': self.slug})


class ProductPhotos(models.Model):
    # product_item = models.ForeignKey(Product, on_delete=models.CASCADE)
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
    type = models.ForeignKey(TypeProduct, on_delete=models.PROTECT)
    brand = models.ForeignKey(BrandProduct, on_delete=models.PROTECT)
    gender = models.ForeignKey(Gender, on_delete=models.PROTECT)
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
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class BasketProduct(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Review(models.Model):
    """Модель отзывов для продукта"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт', related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    comment = models.TextField(max_length=5000)
    parent = models.ForeignKey('self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ['created_at']
