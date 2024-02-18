from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .models import Movies
from .serializers import MovieSerializer
from .pagination import CustomApiPagination
from .filter import MovieFilter
from .permissions import CustomMoviePermission
from omdb_api.helpers import fetch_by_title

class MovieViewSet(viewsets.ModelViewSet):
    """
    Viewset to get, create, update and delete data from database
    """
    queryset = Movies.objects.all().order_by('title')
    serializer_class = MovieSerializer
    permission_classes = [CustomMoviePermission]
    pagination_class = CustomApiPagination
    filterset_class = MovieFilter

    def create(self, request, *args, **kwargs):
        data = request.data
        movie = fetch_by_title(data['title'])
        serializer = self.get_serializer(data=movie)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
