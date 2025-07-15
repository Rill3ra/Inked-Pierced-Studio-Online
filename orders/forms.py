from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'shipping_address', 'city', 'postal_code', 'country', 'phone_number')  # Добавьте все необходимые поля
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'shipping_address': 'Адрес доставки',
            'city': 'Город',
            'postal_code': 'Почтовый индекс',
            'country': 'Страна',
            'phone_number': 'Номер телефона',
        }