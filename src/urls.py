from django.urls import path
from .views import get_notes, query_notes

urlpatterns = [
    path('notes/', get_notes, name='cached_func'),
    path('query_notes/', query_notes)
]
