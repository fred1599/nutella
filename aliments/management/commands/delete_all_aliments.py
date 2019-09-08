from django.core.management.base import BaseCommand

from aliments.models import Aliment


class Command(BaseCommand):
    help = 'Delete all aliments in database'

    def handle(self, *args, **options):
        aliments = Aliment.objects.all().delete()
