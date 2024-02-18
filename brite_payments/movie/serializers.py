from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Movies


class MovieSerializer(serializers.ModelSerializer):
    director = serializers.CharField(allow_blank=True, required=False)
    genre = serializers.CharField(allow_blank=True, required=False)
    imdb_rating = serializers.FloatField(allow_null=True, required=False,
                                         validators=(MinValueValidator(0.0),
                                                     MaxValueValidator(10.0)))
    year = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Movies
        fields = ('id', 'title', 'director', 'genre', 'imdb_rating', 'year')
