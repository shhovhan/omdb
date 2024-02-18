from rest_framework import permissions


class CustomMoviePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.method in ('POST', 'PUT', 'PATCH'):
            return request.user.is_authenticated

        if request.method == 'DELETE':
            return request.user.has_perm('movie.delete_movies')