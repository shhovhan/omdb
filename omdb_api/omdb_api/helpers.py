import requests
from omdb_api.config import API_URL, API_KEY, DB_FIELDS_MAPPING


def fetch_by_title(movie_title):
    movie_data = requests.get(API_URL, params={
                'apiKey': API_KEY,
                't': movie_title
            }).json()
    movie = {DB_FIELDS_MAPPING[k]: movie_data[k] for k in DB_FIELDS_MAPPING}

    return movie


def fetch_by_id(movie_id):
    movie_data = requests.get(API_URL, params={
                'apiKey': API_KEY,
                'i': movie_id
            }).json()
    movie = {DB_FIELDS_MAPPING[k]: movie_data[k] for k in DB_FIELDS_MAPPING}

    return movie

