from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Невероятный тестовый пост',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        task_post = PostModelTest.post.__str__()
        acc_post = PostModelTest.post.text[:15]
        task_group = PostModelTest.group.__str__()
        acc_group = PostModelTest.group.title
        self.assertEqual(task_post, acc_post, 'post __str__ error')
        self.assertEqual(task_group, acc_group, 'group __str__ error')

    def test_verbose_name(self):
        """Проверяем, что verbose_name в полях совпадает с ожидаемым."""
        task_post = PostModelTest.post
        field_verboses = {
            'text': 'напиши что-нибудь классное здесь!',
            'created': 'Дата создания',
            'author': 'Автор',
            'group': 'у поста может быть группа, если захочешь...'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    task_post._meta.get_field(field).verbose_name,
                    expected_value)

    def test_help_text(self):
        """Проверяем, что help_text в полях совпадает с ожидаемым."""
        task_post = PostModelTest.post
        field_help_texts = {
            'text': 'Введите текст поста',
            'group': 'Группа, к которой будет относиться пост'
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    task_post._meta.get_field(field).help_text, expected_value)
