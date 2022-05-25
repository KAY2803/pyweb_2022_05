from rest_framework.test import APITestCase
from blog_api import views
from blog.models import Note
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
from rest_framework.test import APIRequestFactory


class TestBlogApiNoteViews(APITestCase):

    @classmethod
    def setUpTestData(cls):
        test_user_1 = User(
            username="test_user_1",
            password="fake_password1",
        )
        test_user_2 = User(
            username="test_user_2",
            password="fake_password2",
        )
        test_user_1, test_user_2 = User.objects.bulk_create(
            [test_user_1, test_user_2]
        )

        Note(title="test_title_1", message="test_mes_1", author=test_user_1).save()
        Note(title="test_title_2", message="test_mes_2", author=test_user_1).save()
        Note(title="test_title_3", message="test_mes_3", author_id=test_user_2.id).save()
        Note(title="test_title_4", message="test_mes_4", author_id=test_user_2.id).save()

    """ тест на получение пустого списка записей в блоге"""
    def test_empty_NoteListCreateAPIView(self):
        url = reverse('list_notes')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([], response.data)
        # Этот тест работает только если БД пуста, а при текущем setUpTestData это, как я полагаю, невозможно.
        # Варианты: менять БД (без notes)? выносить тест в отдельный класс?
        # Запускать тест при закомиченном setUpTestData? Есть иные варианты?

    """ тест на получение списка записей в блоге"""
    def test_get_NoteListCreateAPIView(self):
        url = reverse('list_notes')
        response = self.client.get(url)
        queryset = Note.objects.values("id", "title", "message", "public", "create_at", "update_at")
        self.assertEqual(queryset.count(), 4)
        self.assertEqual([i for i in queryset], [j for j in response.json()])
        # Последняя проверка выводит ошибку, вероятно, из-за разного формата отображения дат:
        # AssertionError: Lists differ: [{'id[81 chars]at': datetime.datetime(2022, 5, 25, 21, 55, 30[935 chars]
        # tc)}] != [{'id[81 chars]at': '2022-05-25T21:55:30.874600Z', 'update_at[579 chars]: 2}]
        # Есть какой-то способ привести их в единый формат или иной способ проверить
        # полученный список записей блога по содержанию?

    """тест на создание записи в блоге"""
    def test_post_NoteListCreateAPIView(self):
        factory = APIRequestFactory()
        test_user_3 = User.objects.create(username='john')
        view = views.NoteListCreateAPIView.as_view()
        url = reverse('list_notes')
        data = {'title': 'test_title_post', 'message': 'test_mes_post', 'author': test_user_3}
        request = factory.post(url, data)
        force_authenticate(request, user=test_user_3)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Note.objects.get(message__icontains='test_mes_post'))
        self.assertContains(response, 'test_mes_post', status_code=201)

    """Тест на получение существующей записи в блоге"""
    def test_get_exist_note_NoteDetailAPIView(self):
        pk = 3
        url = f'/notes/{pk}'
        queryset = Note.objects.filter(pk=pk).values('id', 'title', 'message', 'public')
        expected_qs = [note for note in queryset]
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_qs, [response.data])

    """Тест на получение несуществующей записи в блоге"""
    def test_get_not_exist_note_NoteDetailAPIView(self):
        pk = 5
        url = f'/notes/{pk}'
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    """Тест на обновление существующей записи в блоге"""
    def test_put_note_NoteDetailAPIView(self):
        pk = 2
        url = f'/notes/{pk}'
        data = {'message': 'test_mes_2_update'}
        request = self.client.put(url, data)
        response = self.client.get(url)
        expected_result = {
            'id': 2,
            'title': 'test_title_2',
            'message': 'test_mes_2_update',
            'public': False
        }
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_result)
        # Последняя проверка выводит ошибку: AssertionError: {'id'[19 chars]_title_2',
        # 'message': "['test_mes_2_update']", 'public': False} != {'id'[19 chars]_title_2',
        # 'message': 'test_mes_2_update', 'public': False}
        # То есть разница в написании 'message'. Не понимаю, почему так происходит?
        # Можно как-то избавиться от этой ошибки?

    """Тест на обновление несуществующей записи в блоге"""
    def test_put_not_exist_note_NoteDetailAPIView(self):
        pk = 75
        url = f'/notes/{pk}'
        data = {'message': "test_mes_75_update"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
