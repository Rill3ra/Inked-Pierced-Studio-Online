from django.urls import path
from . import views

app_name = 'cart'  # Namespace для приложения cart

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),  # Страница корзины
    # Маршрут для добавления товара (принимает product_id)
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    # Маршрут для добавления сертификата (принимает certificate_id)
    path('add_certificate/<int:certificate_id>/', views.cart_add_certificate, name='cart_add_certificate'),
    # Маршрут для обновления количества товара (принимает product_id)
    path('update/<int:product_id>/', views.cart_update, name='cart_update'),
    # Маршрут для удаления товара (принимает item_id)
    path('remove/<int:item_id>/', views.cart_remove, name='cart_remove'),  #  Предполагаем, что item_id - это число
    # Маршрут для очистки всей корзины
    path('clear/', views.cart_clear, name='cart_clear'),
]