from typing import Optional
from django.db.models import QuerySet


def note_filter_author_id(queryset: QuerySet, author_id: Optional[int]):
    """ Фильтруем записи Note по id автора + см как указать КвериСет на Note"""
    if author_id: # проверить интовый тип
        return queryset.filter(author_id=author_id)
    else:
        return queryset