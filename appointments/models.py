from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments', verbose_name='Пользователь')
    date = models.DateField(verbose_name='Дата')
    time = models.TimeField(verbose_name='Время')
    service = models.CharField(max_length=255, verbose_name='Услуга')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    notes = models.TextField(blank=True, verbose_name='Примечания')
    reminder_sent = models.BooleanField(default=False, verbose_name="Напоминание отправлено")  #  <---  Добавьте это поле
    
    def __str__(self):
        return f"Запись: {self.service} - {self.date} {self.time}"

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"