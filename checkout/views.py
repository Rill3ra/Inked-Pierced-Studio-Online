# checkout/views.py
'''
from django.shortcuts import render, redirect
from .models import OrderItem, Order  # Импортируем Order и OrderItem из checkout.models
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required

@login_required
def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user  # Связываем заказ с текущим пользователем
            order.total_price = cart.get_total_price()
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                             product=item['product'],
                                             price=item['price'],
                                             quantity=item['quantity'])
            # Очищаем корзину
            cart.clear()
            # Перенаправляем на страницу подтверждения заказа (или оплаты)
            return redirect('checkout:order_confirmation', order_id=order.id)  # Замените на вашу страницу подтверждения заказа

    else:
        form = OrderCreateForm()  # Создаем экземпляр формы
    return render(request, 'checkout/checkout.html', {'cart': cart, 'form': form})  # Передаем форму в шаблон
'''