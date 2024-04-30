from django.contrib.auth.models import User
from django.db import models


class ImageStorage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default_profile_picture.png', blank=True, upload_to='images/')


class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_notifications = models.BooleanField(default=True)
    proposal_notifications = models.BooleanField(default=True)
    voting_notifications = models.BooleanField(default=True)
