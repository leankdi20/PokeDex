from django.db import models


class Pokemon(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    height = models.FloatField()
    weight = models.FloatField()
    types = models.JSONField()