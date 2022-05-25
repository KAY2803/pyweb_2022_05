from django.test import TestCase
from django.contrib.auth.models import User

from blog.models import Note
from blog_api import filters


class TestBlogAPINoteFilters(TestCase):

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
        # test_user_1.save() не очень хороший момент, т.к. 2 раза обращаемся к базе
        # test_user_2.save()
        test_user_1, test_user_2 = User.objects.bulk_create(
            [test_user_1, test_user_2]
        )

        Note(title="test_title_1", message="test_mes_1", author=test_user_1).save()
        Note(title="test_title_2", message="test_mes_2", author=test_user_1).save()
        Note(title="test_title_2", message="test_mes_3", author_id=test_user_2.id).save()

    def test_note_filter_author_id(self):
        queryset = Note.objects.all()
        filter_author_id = 1

        expected_queryset = queryset.filter(# записи только первого пользователя
            author_id=filter_author_id
        )
        actual_queryset = filters.note_filter_author_id(
            queryset,
            author_id=filter_author_id,
        )

        self.assertQuerysetEqual(
            actual_queryset,
            expected_queryset,
            ordered=False,
        )

    # def test_filter(self):
    #     Note.objects.filter(author__username=...)
    #     Note.objects.filter(author__date_joined__month__gte=...)