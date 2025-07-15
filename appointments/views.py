# appointments/views.py
from django.shortcuts import render, redirect
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Appointment  # Import the Appointment model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def home(request):
    """Отображает главную страницу."""
    return render(request, 'home.html')


@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()

            # Отправка email
            subject = 'Ваша запись на прием успешно создана!'
            context = {
                'appointment': appointment,
                'user': request.user,
            }
            html_message = render_to_string('appointments/appointment_confirmation_email.html', context)
            plain_message = strip_tags(html_message)
            from_email = 'your_email@example.com'  # Замените на вашу почту
            to_email = request.user.email

            send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)

            messages.success(request, 'Запись на прием успешно создана!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Ошибка при создании записи на прием.')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/appointment_create.html', {'form': form})


@login_required
def appointment_list(request):
    """Отображает список записей текущего пользователя."""
    appointments = Appointment.objects.filter(user=request.user).order_by('date', 'time')
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})