import time
from memoize import memoize, delete_memoized
from django.shortcuts import render
from src.models import Note

count = 0

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{func.__name__} took {execution_time} seconds to execute.")
        return result
    return wrapper


@memoize(timeout=60)
@timer
def query_func():
    print("Executing query_func")
    notes = Note.objects.all()
    return [{'name': note.name, 'description': note.description, 'id': note.id} for note in notes]


def cached_func(request):
    global count
    print(f"Count before: {count}")
    if count % 3 == 0:
        print("Deleting memoized")
        delete_memoized(query_func)
    notes_list = query_func()
    print(f"Count after: {count}")
    count += 1
    return render(request, 'cache_func.html', {"data": notes_list})
