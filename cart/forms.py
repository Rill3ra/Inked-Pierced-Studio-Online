# cart/forms.py
from django import forms

class OrderCreateForm(forms.Form):
    first_name = forms.CharField(max_length=100, label='Имя')
    last_name = forms.CharField(max_length=100, label='Фамилия')
    address = forms.CharField(widget=forms.Textarea, label='Адрес')
    # Добавьте другие поля формы, необходимые для заказа

class CartAddProductForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)
    update = forms.BooleanField(required=False,
                                 initial=False,
                                 widget=forms.HiddenInput)