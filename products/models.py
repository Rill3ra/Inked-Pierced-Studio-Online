from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    image = models.ImageField(
        upload_to="categories/",
        blank=True,
        null=True,
        verbose_name="Изображение",
    )
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
        verbose_name="Родительская категория",
    )  # Добавили родительскую категорию

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("products:product_list_by_category", args=[self.slug])


class Product(models.Model):
    CATEGORY_CHOICES = [
        ("piercing", "Пирсинг"),
        ("ear_piercing", "Прокол ушей"),
        ("care", "Средства по уходу"),
        ("tools", "Инструменты"),
    ]

    MATERIAL_CHOICES = [
        ("surgical_steel", "Хирургическая сталь"),
        ("titanium", "Титан"),
        ("gold", "Золото"),
        ("bioplast", "Биопласт"),
    ]

    STYLE_CHOICES = [
        ("minimalism", "Минимализм"),
        ("ethnic", "Этника"),
        ("gothic", "Готика"),
        ("hardcore", "Хардкор"),
    ]

    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена"
    )
    image = models.ImageField(
        upload_to="products/", blank=True, null=True, verbose_name="Изображение"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )
    is_available = models.BooleanField(default=True, verbose_name="В наличии")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлен")
    is_certificate = models.BooleanField(
        default=False, verbose_name="Является сертификатом"
        )

    # Характеристики пирсинга
    piercing_type = models.CharField(
        max_length=255, blank=True, verbose_name="Тип пирсинга"
    )  # Пупок, нос и т.д
    material = models.CharField(
        max_length=20,
        choices=MATERIAL_CHOICES,
        blank=True,
        verbose_name="Материал",
    )
    style = models.CharField(
        max_length=20, choices=STYLE_CHOICES, blank=True, verbose_name="Стиль"
    )
    size = models.CharField(
        max_length=50, blank=True, verbose_name="Размер"
    )  # Например, диаметр кольца
    is_exclusive = models.BooleanField(
        default=False, verbose_name="Эксклюзив"
    )  # Только от дизайнера

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse(
            "products:product_detail", args=[self.category.slug, self.slug]
        )  # Используем slug категории

class Certificate(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена"
    )
    image = models.ImageField(
        upload_to="certificates/%Y/%m/%d", blank=True, verbose_name="Изображение"
    )
    valid_days = models.IntegerField(default=365, verbose_name="Срок действия (дней)")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")

    class Meta:
        verbose_name = "Сертификат"
        verbose_name_plural = "Сертификаты"

    def __str__(self):
        return self.name