import pandas as pd

from django.core.management.base import BaseCommand, CommandError
from omdb_api.config import PREDEFINED_MOVIES_FILE
from omdb_api.helpers import fetch_by_id
from movie.models import Movies


class Command(BaseCommand):

    help = "Extracts data from OMDB API and saves in database"

    def handle(self, *args, **options):
        if Movies.objects.count() == 0:
            df = pd.read_csv(PREDEFINED_MOVIES_FILE, delimiter=';')
            predefined_movies = df['imdb_id'].tolist()
            extracted_movies = []
            for imdb_id in predefined_movies:
                movie = fetch_by_id(imdb_id)
                extracted_movies.append(movie)

            obj_lists = [Movies(**obj_data) for obj_data in extracted_movies]
            Movies.objects.bulk_create(obj_lists)

            self.stdout.write(
                self.style.SUCCESS(
                    f'{len(extracted_movies)} '
                    f'movies successfully added to the database!')
            )
        else:
            CommandError('Database has movies data!')

