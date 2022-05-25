from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    title = models.CharField(max_length=100, default='', verbose_name='Название')
    message = models.TextField(default='', verbose_name='Статья', unique=True)
    public = models.BooleanField(default=False, verbose_name='Статус публикации')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

