from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

from blog.models import Note
from blog_api import serializers, filters

import django
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pyweb_2022_05.settings")
django.setup()


class NoteListCreateAPIView(APIView):
    def get(self, request: Request):
        notes = Note.objects.all()
        serializer = serializers.NoteSerializer(
            instance=notes,
            many=True,
        )
        return Response(data=serializer.data)

    def post(self, request: Request):
        serializer = serializers.NoteSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(data=request.data, status=status.HTTP_201_CREATED)

    # def post(self, request: Request):
    #     data = request.data
    #     note = Note(**data)
    #     note.save(force_insert=True)
    #     return Response(serializers.to_json_post(note), status=status.HTTP_201_CREATED)


# class PublicNotesListAPIView(ListAPIView):
#     queryset = Note.objects.filter(public=True) - не самый лучший способ, т.к. урезается выборка данных
#     serializer_class = serializers.NoteSerializer

class PublicNotesListAPIView(ListAPIView):
    queryset = Note.objects.all()
    serializer_class = serializers.NoteSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(public=True) # можно добавить фильтры, напр. author=self.request.user

    def filter_queryset(self, queryset):
        # queryset = super().filter_queryset(queryset) # это родительская клас фильтр Джанго
        return filters.note_filter_author_id(
            queryset,
            author_id=self.request.query_params.get("author_id", None)
        )


class NoteDetailAPIView(APIView):
    def get(self, request: Request, pk):
        note = get_object_or_404(Note, pk=pk)
        return Response(serializers.to_json_get(note))

    # def put(self, request: Request, pk):
    #     instance = Note.objects.get(pk) # add 404
    #     serialiazer = serializers.NoteSerializer(instance=instance, data=request.data)
    #     serialiazer.save()
    #     return Response(serialiazer) #???

    def put(self, request: Request, pk):
        note = get_object_or_404(Note, pk=pk)
        Note.objects.filter(pk=pk).update(**request.data)
        return Response(serializers.to_json_get(note))


