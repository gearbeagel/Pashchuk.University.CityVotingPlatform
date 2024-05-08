from django.contrib.auth.models import User
from django.db import models

from voting.models import Comment, Project


class ReportOnComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)


class ReportOnProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
