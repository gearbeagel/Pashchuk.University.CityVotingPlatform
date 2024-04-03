from django.contrib.auth.models import User
from django.db import models


class ImageStorage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(null=True, blank=True, upload_to='images/')
