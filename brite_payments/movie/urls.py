from django.urls import path
from .viewset import MovieViewSet

movie_list = MovieViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

movie_detail = MovieViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', movie_list, name='movie-list'),
    path('<int:pk>/', movie_detail, name='movie-detail'),
]