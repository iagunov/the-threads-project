from django.db import models
from django.contrib.auth import get_user_model

from core.models import CreatedModel

User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(CreatedModel):
    title = models.CharField(
        max_length=300,
        verbose_name='Заголовок треда',
        help_text='Будьте конкретны. Представьте, что вы задаёте вопрос другому человеку.'
    )
    text = models.TextField(
        verbose_name='Основная часть',
        help_text='Добавьте всю информацию, которая может понадобиться для ответа на ваш вопрос'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='Метки',
        help_text='Добавьте метки, описывающие о чём ваш вопрос'
    )
    image = models.ImageField(
        'Добавить изображение',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text[:15]


class Comment(CreatedModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий к этому посту'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    text = models.TextField(
        verbose_name='Твой коммент!',
        help_text='Введите текст комментария'
    )
    image = models.ImageField(
        'Добавить изображение',
        upload_to='posts/',
        blank=True
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'author'), name="unique_followers"
            ),
            models.CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='do not self-follow'),
        ]

    def __str__(self):
        return self.text[:15]
