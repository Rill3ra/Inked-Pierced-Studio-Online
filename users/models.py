from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Связь один к одному с User
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True) # Аватар пользователя
    bio = models.TextField(blank=True) # Биография пользователя

    def __str__(self):
        return f'Profile for {self.user.username}'