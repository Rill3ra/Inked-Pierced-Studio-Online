from django import forms
from .models import Appointment
from django.core.exceptions import ValidationError
from django.utils import timezone

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'service', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if date and time:
            # Проверяем, нет ли уже записи на это время
            existing_appointment = Appointment.objects.filter(date=date, time=time).exists()
            if existing_appointment:
                raise ValidationError("Это время уже занято. Пожалуйста, выберите другое время.")

            # Дополнительно: Проверка на выбор будущей даты и времени
            # now = timezone.now().date()
            # if date < now:
            #     raise ValidationError("Нельзя выбрать прошедшую дату.")

        return cleaned_data