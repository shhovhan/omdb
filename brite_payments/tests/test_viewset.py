import json
from django.contrib.auth.models import User, Permission
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from movie.models import Movies
from movie.serializers import MovieSerializer


class TestViewSet(TestCase):

    def setUp(self) -> None:
        self.client = Client()

        self.movie_1 = Movies.objects.create(title='First Test Movie')
        self.movie_2 = Movies.objects.create(title='Second Test Movie')
        self.view_detail = reverse('movie-detail',
                                   kwargs={'pk': self.movie_1.id})
        self.view_list = reverse('movies-list')
        self.user = User.objects.create_user(username='foo', password='bar')

    def test_get_all_movies(self):
        response = self.client.get(self.view_list)
        response_data = response.json()['results']
        movies = Movies.objects.all().order_by('title')
        serializer = MovieSerializer(movies, many=True)

        self.assertEqual(response_data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_single_movie(self):
        response = self.client.get(self.view_detail)
        movie = Movies.objects.get(pk=self.movie_1.id)
        serializer = MovieSerializer(movie)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_movie(self):
        # User not logged in
        response = self.client.post(self.view_list, data={'title': '12 Angry Men'})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # login user
        self.client.login(username='foo', password='bar')

        response = self.client.post(self.view_list, data={'title': '12 Angry Men'})
        expected_data = {
            'id': 3,
            'title': '12 Angry Men',
            'director': 'Sidney Lumet',
            'genre': 'Crime, Drama',
            'imdb_rating': 9.0,
            'year': 1957
        }

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, expected_data)

    def test_put_movie(self):
        data = {
            'title': 'New Test Movie',
            'genre': 'Updated genre',
            'director': 'Updated director',
            'imdb_rating': 8.9,
            'year': 2024
        }
        # User not logged in
        response = self.client.put(self.view_detail, data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # login user
        self.client.login(username='foo', password='bar')

        response = self.client.put(self.view_detail,
                                   data=json.dumps(data),
                                   content_type='application/json')
        expected_data = {
            'id': 1,
            'title': 'New Test Movie',
            'director': 'Updated director',
            'genre': 'Updated genre',
            'imdb_rating': 8.9,
            'year': 2024
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_patch_movie(self):
        data = {
            'director': 'Updated director',
            'imdb_rating': 8.9,
            'year': 2024
        }
        # User not logged in
        response = self.client.patch(self.view_detail, data=data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # login user
        self.client.login(username='foo', password='bar')

        response = self.client.patch(self.view_detail,
                                     data=json.dumps(data),
                                     content_type='application/json')
        expected_data = {
            'id': 1,
            'title': 'First Test Movie',
            'director': 'Updated director',
            'genre': None,
            'imdb_rating': 8.9,
            'year': 2024
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_delete_movie(self):
        # User not logged in
        response = self.client.delete(self.view_detail)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # User logged in but don't have permission to delete
        self.client.login(username='foo', password='bar')
        response = self.client.delete(self.view_detail)

        # Movie is still there
        self.assertEqual(Movies.objects.filter(pk=self.movie_1.id).count(), 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Add delete permission to the user
        delete_perm = Permission.objects.get(codename='delete_movies')
        self.user.user_permissions.add(delete_perm)

        response = self.client.delete(self.view_detail)

        self.assertEqual(Movies.objects.filter(pk=self.movie_1.id).count(), 0)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
