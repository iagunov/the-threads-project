from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Group, Post

User = get_user_model()


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='author')
        cls.not_author = User.objects.create_user(username='not_author')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.author,
            group=cls.group,
            text='Тестовый текст',
            created='14.07.2022',
        )
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.author)
        cls.authorized_client_not_author = Client()
        cls.authorized_client_not_author.force_login(cls.not_author)

    def test_urls_all_users(self):
        """URL-адрес доступен для всех пользователей."""
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': f'/group/{self.group.slug}/',
            'posts/profile.html': f'/profile/{self.author}/',
            'posts/post_detail.html': f'/posts/{self.post.id}/',
        }
        for template, url in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
