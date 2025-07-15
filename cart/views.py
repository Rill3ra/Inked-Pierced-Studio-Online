# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product, Certificate
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from django.contrib import messages
from coupons.models import Coupon
from django.utils import timezone
from django.http import JsonResponse

def cart_detail(request):
    """
    Отображает детали корзины.
    """
    cart = Cart(request)
    coupon_apply_form = CouponApplyForm()
    # coupon = cart.coupon  # Get the coupon from the cart # Удалите эту строку!

    # Формируем список товаров с формами для обновления количества
    items_with_forms = []
    for item in cart:
        item_id = None  # Инициализируем item_id значением по умолчанию
        if 'product' in item:
            item_id = item['product'].id
        elif 'certificate' in item:
            item_id = item['certificate'].id
        else:
            print(f"Пропускаем элемент без продукта или сертификата: {item}")  # Отладочное сообщение
            continue  # Пропускаем "битый" элемент

        # Теперь item_id всегда определен (либо None, либо ID продукта/сертификата)
        if item_id:  # Проверяем, что item_id не None
            item['update_quantity_form'] = CartAddProductForm(
                initial={'quantity': item['quantity'], 'update': True}
            )
            items_with_forms.append(item)

    # Передаем все необходимые данные в шаблон
    return render(
        request,
        'cart/cart_detail.html',
        {
            'cart': items_with_forms,
            'coupon_apply_form': coupon_apply_form,
            # 'coupon': coupon,  # Pass the coupon to the template # Удалите эту строку!
        }
    )

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(item=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['update'])
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, item_id):
    cart = Cart(request)
    cart.remove(item_id)
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    """
    Обновляет количество товара в корзине и возвращает JSON ответ с обновленными данными.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(item=product,
                 quantity=cd['quantity'],
                 override_quantity=cd['update'])

        # Получаем обновленные значения из корзины
        total_price = cart.get_total_price()
        discount = cart.get_discount()
        total_after_discount = cart.get_total_price_after_discount()

        # Формируем JSON ответ
        return JsonResponse({
            'total_price': str(total_price),  # Преобразуем в строку
            'discount': str(discount),  # Преобразуем в строку
            'total_after_discount': str(total_after_discount),  # Преобразуем в строку
        })
    else:
        return JsonResponse({'error': form.errors}, status=400)

def cart_clear(request):  # <----  ДОБАВЬТЕ ЭТУ ФУНКЦИЮ
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')

@require_POST
def cart_add_certificate(request, certificate_id):
    cart = Cart(request)
    certificate = get_object_or_404(Certificate, id=certificate_id)
    cart.add(item=certificate)
    return redirect('cart:cart_detail')

@require_POST  # Ensure CouponApplyForm is used
def coupon_apply(request):
    cart = Cart(request)
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code,
                                         valid_from__lte=timezone.now(),
                                         valid_to__gte=timezone.now(),
                                         active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
            messages.error(request, "Недействительный купон")
    return redirect('cart:cart_detail')