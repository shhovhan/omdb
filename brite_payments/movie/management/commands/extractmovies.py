import pandas as pd
import requests

from django.core.management.base import BaseCommand, CommandError
from omdb_api.config import API_KEY, API_URL, PREDEFINED_MOVIES_FILE, DB_FIELDS_MAPPING

from movie.models import Movies


class Command(BaseCommand):

    help = "Extracts data from OMDB API and saves in database"

    def handle(self, *args, **options):
        if Movies.objects.count() == 0:
            df = pd.read_csv(PREDEFINED_MOVIES_FILE, delimiter=';')
            predefined_movies = df['imdb_id'].tolist()
            extracted_movies = []
            for imdb_id in predefined_movies:
                movie = requests.get(API_URL, params={
                    'apiKey': API_KEY,
                    'i': imdb_id
                }).json()
                mv = {DB_FIELDS_MAPPING[k]: movie[k] for k in DB_FIELDS_MAPPING}
                extracted_movies.append(mv)

            obj_lists = [Movies(**obj_data) for obj_data in extracted_movies]
            Movies.objects.bulk_create(obj_lists)
        else:
            CommandError('Database has movies data!')

        self.stdout.write(
            self.style.SUCCESS(f'{len(extracted_movies)} successfully added to the database!')
        )
