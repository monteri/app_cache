from celery import shared_task
from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator

from src.models import Note


@shared_task
def cache_page(page):
    print("Caching page", page)
    notes = Note.objects.all()
    paginator = Paginator(notes, settings.NOTE_PAGE_SIZE)
    page_obj = paginator.get_page(page)
    cache_key = f'notes_page_{page}'
    cached_data = {
        'notes_list': [{'name': note.name, 'description': note.description, 'id': note.id} for note in
                       page_obj.object_list],
        'number': page_obj.number,
        'has_next': page_obj.has_next(),
        'has_previous': page_obj.has_previous(),
        'num_pages': page_obj.paginator.num_pages,
    }
    print(cached_data)
    cache.set(cache_key, cached_data, 60)
