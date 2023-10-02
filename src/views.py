import time

from django.core.cache import cache
from django.http import Http404
from django.shortcuts import render

from src.tasks import cache_page


def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{func.__name__} took {execution_time} seconds to execute.")
        return result
    return wrapper


def query_notes(page):
    print("Executing query_func")
    cache_key = f'notes_page_{page}'
    cached_data = cache.get(cache_key)

    if cached_data is None:
        # Start the task to cache the data
        cache_page.delay(page)
        return {"loading": True}

    data = {
        "loading": False,
        **cached_data,
    }

    return data


def get_notes(request):
    page = request.GET.get('page', 1)
    print(f'{page=}')
    try:
        page = int(page)
        if page <= 0:
            raise ValueError("Invalid page number")
    except ValueError:
        raise Http404("Invalid page number")

    data = query_notes(page)
    print(f'{data=}')
    return render(request, 'cache_func.html', data)
