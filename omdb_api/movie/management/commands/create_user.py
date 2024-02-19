from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Permission
from django.db import IntegrityError


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            user = User.objects.create_user(username='test_user',
                                            email='test@user.com',
                                            password='testuser123')

            # Add delete permission to the user
            delete_perm = Permission.objects.filter(codename='delete_movies')
            user.user_permissions.add(delete_perm)

            self.stdout.write(
                self.style.SUCCESS(f'User {user.username} has been created.')
            )
        except IntegrityError:
            CommandError('User already exist')
