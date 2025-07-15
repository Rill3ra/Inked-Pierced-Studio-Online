# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistrationForm, LoginForm, ProfileEditForm, ProfileAvatarForm, CustomPasswordChangeForm  # Import new form
from .models import Profile  # Импортируем модель Profile
from django.contrib.auth.models import User
from appointments.models import Appointment


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем пользователя
            Profile.objects.create(user=user)  # Создаём профиль для пользователя
            login(request, user)  # Автоматически логиним пользователя после регистрации
            messages.success(request, 'Registration successful!')
            return redirect('home')  # Перенаправляем на главную страницу
        else:
            messages.error(request, 'Registration failed.')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Login failed.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'Logged out successfully!')
    return redirect('home')


@login_required
def profile(request):
    try:
        profile = request.user.profile  # Попытка получить профиль
    except Profile.DoesNotExist:
        # Если профиля нет, создаем его
        Profile.objects.create(user=request.user)
        profile = request.user.profile

    appointments = Appointment.objects.filter(user=request.user)  # Получаем записи пользователя

    if request.method == 'POST':
        user_form = ProfileEditForm(request.POST, instance=request.user)
        avatar_form = ProfileAvatarForm(request.POST, request.FILES, instance=profile)  # Используем profile здесь
        password_form = CustomPasswordChangeForm(request.POST, user=request.user, request=request)  # Pass request

        if user_form.is_valid() and avatar_form.is_valid() and password_form.is_valid():
            user_form.save()
            avatar_form.save()
            password_form.save()  # Save password form
            update_session_auth_hash(request, request.user)  # Обновляем сессию
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Profile update failed.')
            context = {'user_form': user_form, 'avatar_form': avatar_form, 'profile': profile,
                       'password_form': password_form, 'appointments': appointments}  # Передаем form и appointments в контекст
            return render(request, 'users/profile.html', context)  # Возвращаем контекст при ошибке
    else:
        user_form = ProfileEditForm(instance=request.user)
        avatar_form = ProfileAvatarForm(instance=profile)  # Используем profile здесь
        password_form = CustomPasswordChangeForm(user=request.user, request=request)  # Pass request

        context = {'user_form': user_form, 'avatar_form': avatar_form, 'profile': profile,
                   'password_form': password_form, 'appointments': appointments}  # Передаем form и appointments в контекст
        return render(request, 'users/profile.html', context)  # Возвращаем контекст при GET запросе