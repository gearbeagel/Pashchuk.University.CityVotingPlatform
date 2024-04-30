from django.contrib.auth.models import User
from django.db import models


class UserSubmission(models.Model):
    DISTRICT_CHOICES = [
        ('Galician District', 'Galician District'),
        ('Frankivskyi District', 'Frankivskyi District'),
        ('Lychakivskyi District', 'Lychakivskyi District'),
        ('Shevchenkivskyi District', 'Shevchenkivskyi District'),
        ('Sykhivskyi District', 'Sykhivskyi District'),
        ('Zaliznychnyi District', 'Zaliznychnyi District'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=200)
    description = models.TextField()
    district = models.CharField(max_length=50, choices=DISTRICT_CHOICES, default='Galician District')
    is_approved = models.BooleanField(default=False)
