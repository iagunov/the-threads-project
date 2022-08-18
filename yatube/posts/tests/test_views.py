from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, Client
from django.urls import reverse
from django import forms

from ..models import Post, Group

User = get_user_model()


class TaskPagesTests(TestCase):
    # создаем пользователя
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='myuser'
        )
        cls.user_follow = User.objects.create_user(
            username='myuser-follow'
        )
        cls.user_follow_feed = User.objects.create_user(
            username='myuser-follow-feed'
        )
        # создаем тестовую группу поста
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        # создаем тестовый пост
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый текст',
            created='14.07.2022',
        )
        # авторизуем пользователя
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.authorized_client_feed = Client()
        cls.authorized_client_feed.force_login(cls.user_follow)
        cls.auth_client_feed = Client()
        cls.auth_client_feed.force_login(cls.user_follow_feed)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        cache.clear()
        templates_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            (reverse(
                'posts:post_create'
            )): 'posts/create_post.html',
            (reverse(
                'posts:group_list',
                kwargs={'slug': f'{self.post.group.slug}'}
            )): 'posts/group_list.html',
            (reverse(
                'posts:post_detail',
                kwargs={'post_id': f'{self.post.pk}'}
            )): 'posts/post_detail.html',
            (reverse(
                'posts:post_edit',
                kwargs={'post_id': f'{self.post.pk}'}
            )): 'posts/create_post.html',
            (reverse(
                'posts:profile',
                kwargs={'username': f'{self.post.author}'}
            )): 'posts/profile.html',
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_not_found(self):
        """Запрос к несуществующей странице вернет ошибку
        и вызовет кастомный шаблон
        """
        response = self.authorized_client.get(
            '/not-exist/'
        )
        self.assertEqual(
            response.status_code,
            HTTPStatus.NOT_FOUND
        )
        self.assertTemplateUsed(
            response, 'core/404.html'
        )

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован
        с правильным контекстом.
        """
        cache.clear()
        response = (self.authorized_client.get(
            reverse('posts:index')))
        post = response.context['page_obj'][0].text
        self.assertEqual(post, 'Тестовый текст')

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован
        с правильным контекстом.
        """
        response = (self.authorized_client.get(
            reverse('posts:group_list',
                    kwargs={'slug': 'test_slug'})))
        group = (response.context
                 ['page_obj'][0].group.title)
        self.assertEqual(group, 'Тестовая группа')

    def test_user_list_page_show_correct_context(self):
        """Шаблон profile сформирован
        с правильным контекстом.
        """
        response = (self.authorized_client.get(
            reverse('posts:profile',
                    kwargs={'username': 'myuser'})))
        user = response.context['page_obj'][0].author
        self.assertEqual(user, self.user)

    def test_post_detail_list_page_show_correct_context(self):
        """Шаблон post_detail сформирован
        с правильным контекстом.
        """
        response = (self.authorized_client.get(
            reverse('posts:post_detail',
                    kwargs={'post_id': '1'})))
        post_detail = response.context['post'].text
        self.assertEqual(post_detail, 'Тестовый текст')

    def test_post_create_list_page_show_correct_context(self):
        """Шаблон post_create сформирован
        с правильным контекстом.
        """
        response = (self.authorized_client.get(
            reverse('posts:post_create')))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = (
                    response.context.get('form').fields.get(
                        value))
                self.assertIsInstance(form_field, expected)

    def test_post_edit_list_page_show_correct_context(self):
        """Шаблон post_edit сформирован
        с правильным контекстом.
        """
        response = (self.authorized_client.get(
            reverse('posts:post_edit',
                    kwargs={'post_id': '1'})))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = (
                    response.context.get('form').fields.get(value)
                )
                self.assertIsInstance(form_field, expected)

    def test_post_with_group_index_show_correct_context(self):
        """Пост с группой есть на главной странице."""
        cache.clear()
        response = (
            self.authorized_client.get(reverse('posts:index')))
        post = response.context['page_obj'][0]
        post_text = post.text
        post_group = post.group.title
        post_author = post.author.username
        self.assertEqual(post_text, 'Тестовый текст')
        self.assertEqual(post_group, 'Тестовая группа')
        self.assertEqual(post_author, 'myuser')

    def test_post_with_group_list_show_correct_context(self):
        """Пост с группой есть на странице с группой."""
        response = (self.authorized_client.get(
            reverse('posts:group_list',
                    kwargs={'slug': 'test_slug'})))
        post = response.context['page_obj'][0]
        post_text = post.text
        post_group = post.group.title
        post_author = post.author.username
        self.assertEqual(post_text, 'Тестовый текст')
        self.assertEqual(post_group, 'Тестовая группа')
        self.assertEqual(post_author, 'myuser')

    def test_post_with_group_profile_show_correct_context(self):
        """Пост с группой есть на странице пользователя."""
        response = (
            self.authorized_client.get(
                reverse(
                    'posts:profile',
                    kwargs={'username': 'myuser'}
                )
            )
        )
        post = response.context['page_obj'][0]
        post_text = post.text
        post_group = post.group.title
        post_author = post.author.username
        self.assertEqual(post_text, 'Тестовый текст')
        self.assertEqual(post_group, 'Тестовая группа')
        self.assertEqual(post_author, 'myuser')

    def test_user_follow(self):
        """Авторизованный пользователь может подписываться
        на других пользователей и удалять их из подписок.
        """
        self.authorized_client.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': 'myuser-follow'}
            )
        )
        response_profile = (
            self.authorized_client.get(
                reverse(
                    'posts:profile',
                    kwargs={'username': 'myuser-follow'}
                )
            )
        )
        follow = response_profile.context
        self.assertEqual(follow['following'], True)

        self.authorized_client.get(
            reverse(
                'posts:profile_unfollow',
                kwargs={'username': 'myuser-follow'}
            )
        )

        response_profile = (
            self.authorized_client.get(
                reverse(
                    'posts:profile',
                    kwargs={'username': 'myuser-follow'}
                )
            )
        )
        follow = response_profile.context
        self.assertEqual(follow['following'], False)

    def test_follow_feed(self):
        """Новая запись пользователя появляется
        в ленте тех, кто на него подписан и не
        появляется в ленте тех, кто не подписан.
        """
        self.authorized_client_feed.get(
            reverse(
                'posts:profile_follow',
                kwargs={'username': 'myuser'}
            )
        )
        response_index = (
            self.authorized_client_feed.get(
                reverse(
                    'posts:follow_index'
                )
            )
        )
        follow_index = response_index.context['page_obj'][0]
        self.assertEqual(follow_index.text, 'Тестовый текст')

        response_index_unfollow = (
            self.auth_client_feed.get(
                reverse(
                    'posts:follow_index'
                )
            )
        )
        follow_index_feed = response_index_unfollow.context['page_obj']
        self.assertEqual(len(follow_index_feed), 0)


class PaginatorTests(TestCase):
    # создаем пользователя
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='myuser')
        # создаем тестовую группу поста
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        # генерируем 13 постов
        for i in range(0, 13):
            cls.post = Post.objects.create(
                author=cls.user,
                group=cls.group,
                text='Тестовый текст',
                created='14.07.2022',
            )
        # авторизируем пользователя
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_first_page_index(self):
        """Index - На первой странице должно быть 10 постов"""
        cache.clear()
        response = self.authorized_client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_index(self):
        """Index - На второй странице должно быть 3 поста"""
        response = (self.authorized_client.get(
            reverse('posts:index') + '?page=2'))
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_first_group_list(self):
        """Group_list - На первой странице должно быть 10 постов"""
        response = (self.authorized_client.get(
            reverse('posts:group_list',
                    kwargs={'slug': 'test_slug'})))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_group_list(self):
        """Group_list - На второй странице должно быть 3 поста"""
        response = (self.authorized_client.get(
            reverse('posts:group_list',
                    kwargs={'slug': 'test_slug'}) + '?page=2'))
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_first_profile(self):
        """Profile - На первой странице должно быть 10 постов"""
        response = (self.authorized_client.get(
            reverse('posts:profile',
                    kwargs={'username': 'myuser'})))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_profile(self):
        """Profile - На второй странице должно быть 3 поста"""
        response = (self.authorized_client.get(
            reverse('posts:profile',
                    kwargs={'username': 'myuser'}) + '?page=2'))
        self.assertEqual(len(response.context['page_obj']), 3)
