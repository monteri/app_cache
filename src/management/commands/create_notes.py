from django.core.management.base import BaseCommand
from src.models import Note
import random
import string


class Command(BaseCommand):
    help = 'Create random notes'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of notes to be created')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        for i in range(total):
            Note.objects.create(
                name=''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
                description=''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=255))
            )
        self.stdout.write(self.style.SUCCESS(f'{total} notes created!'))