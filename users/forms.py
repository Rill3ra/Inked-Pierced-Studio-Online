from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import authenticate


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email') # Добавляем email в форму регистрации


class LoginForm(AuthenticationForm):
    pass  # Используем стандартную форму аутентификации


class ProfileEditForm(UserChangeForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class ProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('avatar', 'bio')

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Текущий пароль")
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="Новый пароль")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Подтвердите новый пароль")

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        user = self.request.user  # Получите пользователя из запроса
        if not authenticate(username=user.username, password=old_password):
            raise forms.ValidationError('Неверный текущий пароль.')
        return old_password

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None) # Add request to init
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})