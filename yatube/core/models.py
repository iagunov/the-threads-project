from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания."""
    created = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        # Это абстрактная модель:
        abstract = True


class Publication(CreatedModel):
    title = models.CharField(
        max_length=300,
        verbose_name='Заголовок треда',
        help_text='Будьте конкретны. Представьте, что вы задаёте вопрос другому человеку.',
        default='Заголовок по умолчанию'
    )
    text = models.TextField(
        verbose_name='Основная часть',
        help_text='Добавьте всю информацию, которая может понадобиться для ответа на ваш вопрос'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        abstract = True