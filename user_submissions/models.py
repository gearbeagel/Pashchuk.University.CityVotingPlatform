from django.db import models


class UserSubmission(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    is_approved = models.BooleanField(default=False)
