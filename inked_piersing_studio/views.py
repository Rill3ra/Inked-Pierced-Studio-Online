from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
import os
from datetime import datetime

def home(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        service = request.POST.get('service')

        try:
            appointment_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        except ValueError:
            return render(request, 'home.html', {'error_message': "Неверный формат даты или времени."})

        filename = appointment_datetime.strftime("%Y%m%d_%H%M%S") + ".txt"
        filepath = os.path.join(settings.BASE_DIR, 'appointments', filename)

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Имя: {name}\n")
                f.write(f"Email: {email}\n")
                f.write(f"Телефон: {phone}\n")
                f.write(f"Дата: {date}\n")
                f.write(f"Время: {time}\n")
                f.write(f"Услуга: {service}\n")
            return render(request, 'home.html', {'success_message': "Запись успешно забронирована!"})
        except Exception as e:
            return render(request, 'home.html', {'error_message': f"Ошибка при сохранении записи: {e}"})

    return render(request, 'home.html')  # Отображение главной страницы (GET-запрос)

def about_us(request):
    """
    Отображает страницу "О нас".
    """
    return render(request, 'about.html')