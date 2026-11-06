from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=50)
    year = models.IntegerField()
    genre = models.CharField(max_length=100)
