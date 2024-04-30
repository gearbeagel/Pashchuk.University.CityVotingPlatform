from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User


# Project class
class Project(models.Model):
    DISTRICT_CHOICES = [
        ('Galician District', 'Galician District'),
        ('Frankivskyi District', 'Frankivskyi District'),
        ('Lychakivskyi District', 'Lychakivskyi District'),
        ('Shevchenkivskyi District', 'Shevchenkivskyi District'),
        ('Sykhivskyi District', 'Sykhivskyi District'),
        ('Zaliznychnyi District', 'Zaliznychnyi District'),
    ]

    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    description = models.TextField()
    district = models.CharField(max_length=50, choices=DISTRICT_CHOICES, default='Galician District')
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        Vote.objects.create(project=self, choice_text='Approve')
        Vote.objects.create(project=self, choice_text='Disapprove')


# Vote class
class Vote(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


# Comment class
class Comment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.project.name}'


# User Choice class to associate users with their votes for each project
class UserChoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    vote = models.ForeignKey(Vote, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return self.vote.choice_text
