from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),  # Главная страница продуктов (список всех)
    path('search/', views.product_search, name='product_search'),  # Поиск продуктов
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),  # Список продуктов по категории
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),  # Детальная страница продукта
    path('certificates/<int:certificate_id>/', views.certificate_detail, name='certificate_detail'),
]