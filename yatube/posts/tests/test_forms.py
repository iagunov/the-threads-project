import shutil
import tempfile
from http import HTTPStatus

from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from ..forms import CommentForm, PostForm
from ..models import Comment, Group, Post, User

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='author')
        cls.group_1 = Group.objects.create(
            title='Тестовая группа',
            slug='test_slug',
            description='Тестовое описание',
        )
        cls.group_2 = Group.objects.create(
            title='новая тестовая группа',
            slug='new_test_slug',
            description='Тестовое описание',
        )
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(
            author=cls.author,
            group=cls.group_1,
            text='Тестовый текст',
            created='14.07.2022',
            image=uploaded,
        )

        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.author)
        cls.guest = Client()
        cls.form = PostForm()
        cls.form_comment = CommentForm()

    @classmethod
    def tearDownClass(cls):
        cache.clear()
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def test_edit_post(self):
        """Измененный Post записывается в базу."""
        update_url = reverse('posts:post_edit', args=('1',))

        response_guest = self.guest.get(update_url)
        self.assertEqual(response_guest.status_code, HTTPStatus.FOUND)

        response_auth = self.authorized_client.get(update_url)
        form = response_auth.context['form']
        data = form.initial
        data['text'] = 'Новый тестовый текст'

        self.authorized_client.post(update_url, data)
        self.authorized_client.get(update_url)

        self.assertTrue(
            Post.objects.filter(
                text='Новый тестовый текст',
            ).exists()
        )
        response_auth = self.authorized_client.get(update_url)
        form = response_auth.context['form']
        data = form.initial
        data['group'] = 2
        self.authorized_client.post(update_url, data)
        self.authorized_client.get(update_url)
        self.assertTrue(
            Post.objects.filter(
                group=self.group_2,
            ).exists()
        )
        get_group_list = reverse(
            'posts:group_list',
            kwargs={'slug': 'test_slug'})
        response = self.authorized_client.get(
            get_group_list)
        group = (response.context
                 ['page_obj'])
        self.assertEqual(len(group), 0)

    def test_img_context_index(self):
        """Шаблон index сформирован с картинкой."""
        cache.clear()
        response = (self.authorized_client.get(
            reverse('posts:index')))
        post = response.context['page_obj'][0].image.name
        self.assertEqual(post, 'posts/small.gif')

    def test_img_context_profile(self):
        """Шаблон profile сформирован с картинкой."""
        response = (self.authorized_client.get(
            reverse('posts:profile',
                    kwargs={'username': 'author'})))
        post = response.context['page_obj'][0].image.name
        self.assertEqual(post, 'posts/small.gif')

    def test_img_context_group(self):
        """Шаблон group сформирован с картинкой."""
        response = (self.authorized_client.get(
            reverse('posts:group_list',
                    kwargs={'slug': 'test_slug'})))
        post = response.context['page_obj'][0].image.name
        self.assertEqual(post, 'posts/small.gif')

    def test_img_context_detail(self):
        """Шаблон detail сформирован с картинкой."""
        response = (self.authorized_client.get(
            reverse('posts:post_detail',
                    kwargs={'post_id': '1'})))
        post = response.context['post'].image.name
        self.assertEqual(post, 'posts/small.gif')

    def test_comment_auth(self):
        """Коммент создается только авторизированным
        пользователем и отображается в контексте
        страницы post_detail.
        """
        get_comment = reverse(
            'posts:post_detail',
            kwargs={'post_id': '1'}
        )
        response = self.authorized_client.get(get_comment)

        form = response.context['form']
        data = form.initial
        data['text'] = 'Тестовый коммент'

        response = self.authorized_client.post(
            reverse('posts:add_comment', kwargs={'post_id': '1'}),
            data=data,
            follow=True
        )
        # коммент существует в контексте страницы
        self.assertEqual(
            response.context['comments'][0].text,
            'Тестовый коммент'
        )
        self.assertTrue(
            Comment.objects.filter(
                text='Тестовый коммент',
            ).exists()
        )
        # не авторизированный пользователь получает редирект
        response_guest = self.guest.get(reverse(
            'posts:add_comment',
            kwargs={'post_id': '1'})
        )
        self.assertEqual(response_guest.status_code, HTTPStatus.FOUND)
        # количество комментов не изменилось
        self.assertEqual(Comment.objects.count(), 1)

    def test_cache_index(self):
        """Проверка хранения и очищения кэша для index."""
        response = self.authorized_client.get(reverse('posts:index'))
        posts = response.content

        Post.objects.create(
            text='test_new_post',
            author=self.author,
        )
        response_old = self.authorized_client.get(reverse('posts:index'))
        old_posts = response_old.content

        self.assertEqual(old_posts, posts)

        cache.clear()

        response_new = self.authorized_client.get(reverse('posts:index'))
        new_posts = response_new.content

        self.assertNotEqual(old_posts, new_posts)

    def test_create_post(self):
        """Валидная форма создает запись в Posts."""
        Post.objects.all().delete()
        self.assertEqual(Post.objects.count(), 0)

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='new_small.gif',
            content=small_gif,
            content_type='image/gif'
        )

        form_data = {
            'text': 'Тестовый текст',
            'image': uploaded,
        }

        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )

        self.assertRedirects(
            response, reverse(
                'posts:profile', kwargs={'username': 'author'}
            )
        )
        self.assertEqual(Post.objects.count(), 1)
        # картинка из формы создалась и существует
        self.assertTrue(
            Post.objects.filter(
                text=form_data['text'],
                image='posts/new_small.gif',
            ).exists()
        )
