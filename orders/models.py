from django.db import models
from django.conf import settings
from products.models import Product  # Предполагаем, что у тебя есть приложение products

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders', verbose_name='Пользователь')
    first_name = models.CharField(max_length=50, verbose_name='Имя', blank=True)
    last_name = models.CharField(max_length=50, verbose_name='Фамилия', blank=True)
    email = models.EmailField(verbose_name='Email', blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефона')  # Необязательное поле для номера телефона
    shipping_address = models.CharField(max_length=250, verbose_name='Адрес доставки', blank=True)
    city = models.CharField(max_length=100, verbose_name='Город', blank=True)
    postal_code = models.CharField(max_length=20, verbose_name='Почтовый индекс', blank=True)
    country = models.CharField(max_length=100, verbose_name='Страна', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)


    class Meta:
        ordering = ('-created_at',)  # Сортировка по дате создания (от новых к старым)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Order #{self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена на момент заказа
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} in Order #{self.order.id}'

    def get_cost(self):
        return self.price * self.quantity