# orders/tasks.py (если используете Celery)
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


@shared_task  # Если используете Celery
def send_order_confirmation_email_task(order_id):
    from .models import Order # Импортируем Order здесь чтобы избежать циклических зависимостей
    order = Order.objects.get(pk=order_id)
    subject = f'Подтверждение заказа №{order.id}'
    from_email = settings.DEFAULT_FROM_EMAIL  # Берем из settings.py
    to_email = order.email  # Используем email из модели Order

    # Создаем HTML версию письма
    html_content = render_to_string('emails/order_confirmation.html', {'order': order})

    # Создаем текстовую версию письма (для клиентов, которые не могут просматривать HTML)
    text_content = strip_tags(html_content)  # Убираем HTML теги

    # Создаем объект EmailMultiAlternatives
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# orders/utils.py (если НЕ используете Celery)
"""
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_order_confirmation_email(order):
    subject = f'Подтверждение заказа №{order.id}'
    from_email = settings.DEFAULT_FROM_EMAIL  # Берем из settings.py
    to_email = order.email  # Используем email из модели Order

    # Создаем HTML версию письма
    html_content = render_to_string('emails/order_confirmation.html', {'order': order})

    # Создаем текстовую версию письма (для клиентов, которые не могут просматривать HTML)
    text_content = strip_tags(html_content)  # Убираем HTML теги

    # Создаем объект EmailMultiAlternatives
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()"""