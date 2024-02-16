from django.db import models


class Movies(models.Model):
    title = models.CharField(max_length=50)
    director = models.CharField(max_length=20, blank=True, null=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    imdb_rating = models.FloatField(blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
