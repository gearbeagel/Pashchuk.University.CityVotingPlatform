from django.db import models


class DistrictInfo(models.Model):
    name = models.CharField(max_length=200)
    population = models.IntegerField()
    area = models.IntegerField()
    administration = models.CharField(max_length=200)
    administration_contact = models.URLField(max_length=200)

    def __str__(self):
        return self.name
