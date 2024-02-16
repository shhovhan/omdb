from rest_framework import serializers

from .models import Movies


class MovieSerializer(serializers.ModelSerializer):
    director = serializers.CharField(required=False)
    genre = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    imdb_rating = serializers.FloatField(allow_null=True, required=False)
    year = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Movies
        fields = ('id', 'title', 'director', 'genre', 'imdb_rating', 'year')
