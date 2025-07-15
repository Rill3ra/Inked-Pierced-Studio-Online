from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import OrderItem, Order
from .forms import OrderCreateForm
from products.models import Product  # Предполагаем, что у тебя есть приложение products
from django.http import HttpResponseRedirect
from cart.cart import Cart  # Импортируем класс Cart
from cart.forms import CartAddProductForm  # Импортируем класс CartAddProductForm

# Импортируем функцию отправки письма (выберите правильный импорт)
from .utils import send_order_confirmation_email  # Если НЕ используете Celery
#from .tasks import send_order_confirmation_email_task # Если используете Celery


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False) # Создаем объект Order, но не сохраняем его в базу данных
            order.user = request.user  # Устанавливаем текущего пользователя
            order.save() # Сохраняем заказ

            # Создаем элементы заказа на основе товаров в корзине
            for item in cart:
                product = item.get('product') # get product

                if product: # Check that product is not None
                    OrderItem.objects.create(order=order,
                                             product=product,
                                             price=item['price'],
                                             quantity=item['quantity'])
                else:
                  # Handle the case where there is no product (e.g., a certificate)
                  print("Skipping order item creation due to missing product.")

            # Очищаем корзину
            cart.clear()
            messages.success(request, 'Order created successfully!')

            # Отправляем письмо (ВЫБЕРИТЕ ПРАВИЛЬНЫЙ ВЫЗОВ):
            #send_order_confirmation_email(order)  # Если НЕ используете Celery
            send_order_confirmation_email(order) # Если используете Celery, вызываем задачу асинхронно

            # Перенаправляем на страницу подтверждения заказа
            return redirect('orders:order_confirmation', order_id=order.id)
    else:
        form = OrderCreateForm()

    return render(request, 'orders/order_create.html', {'form': form, 'cart': cart})

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_confirmation.html', {'order': order})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)  # Убеждаемся, что заказ принадлежит текущему пользователю
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'orders/order_detail.html', {'order': order, 'order_items': order_items})  # Передаем order_items в шаблон

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})