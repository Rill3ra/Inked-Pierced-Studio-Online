#coupon/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
        )
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
    
    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to