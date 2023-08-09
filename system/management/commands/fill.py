from django.core.management import BaseCommand, call_command

from system.models import System


class Command(BaseCommand):
    help = 'Fill database with new data'

    def handle(self, *args, **options):
        System.objects.all().delete()
        call_command('loaddata', 'fixture.json')

