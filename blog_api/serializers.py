from rest_framework import serializers

from blog.models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'
        read_only_fields = ('author',)


def to_json_get(note):
    return {
        'id': note.id,
        'title': note.title,
        'message': note.message,
        'public': note.public
    }


def to_json_post(note):
    return {
        'title': note.title,
        'message': note.message,
        'public': note.public
    }
