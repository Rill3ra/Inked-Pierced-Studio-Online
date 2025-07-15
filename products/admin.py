from django.contrib import admin
from .models import Category, Product, Certificate

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'description', 'image']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['parent']  # Фильтр по родительской категории


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'material', 'style', 'piercing_type', 'is_exclusive', 'created_at']
    list_filter = ['category', 'is_available', 'material', 'style', 'is_exclusive']
    list_editable = ['price', 'is_available']
    prepopulated_fields = {'slug': ('name',)}
    #search_fields = ['name', 'description']


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'valid_days', 'created']