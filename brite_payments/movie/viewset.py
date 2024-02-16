from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from .models import Movies
from .serializers import MovieSerializer
from rest_framework.pagination import PageNumberPagination


class MovieViewSet(viewsets.ViewSet):
    """
    Viewset to get, create, update and delete data from database
    """
    pagination_class = PageNumberPagination

    def list(self, request):
        paginator = self.pagination_class()
        # if request.GET.get('limit'):
        #     paginate_by = request.GET.get('limit', 10)
        data = paginator.paginate_queryset(Movies.objects.all().order_by('title'), request)
        serializer = MovieSerializer(data, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            data = Movies.objects.get(pk=pk)
        except Movies.DoesNotExist:
            return Response({'message': f'Movie {pk} does not exist'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        data = request.data
        serializer = MovieSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            movie = Movies.objects.get(pk=pk)
        except Movies.DoesNotExist:
            return Response({'message': f'Movie {pk} does not exist'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def partial_update(self, request, pk=None):
        try:
            movie = Movies.objects.get(pk=pk)
        except Movies.DoesNotExist:
            return Response({'message': f'Movie {pk} does not exist'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = MovieSerializer(movie, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({'message': f'User is not authenticated'},
                            status=status.HTTP_403_FORBIDDEN)
        try:
            movie = Movies.objects.get(pk=pk)
        except Movies.DoesNotExist:
            return Response({'message': f'Movie {pk} does not exist'},
                            status=status.HTTP_404_NOT_FOUND)
        movie.delete()
        return Response([], status=status.HTTP_200_OK)
