import os

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Delete all users in database'

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            if user.username != os.environ.get('ADMIN'):
                user.delete()
