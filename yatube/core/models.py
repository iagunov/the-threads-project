from django.contrib.auth import get_user_model
from django.db import models
from mdeditor.fields import MDTextField

User = get_user_model()


class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания."""
    created = models.DateTimeField(
        'Дата создания',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        # Это абстрактная модель:
        abstract = True


class Publication(CreatedModel):
    title = models.CharField(
        max_length=1000,
        verbose_name='Название',
        default='Заголовок',
    )
    text = MDTextField(
        verbose_name=('Будьте конкретны. Представьте, '
                      'что вы задаёте вопрос или пытаетесь продать что-то другому человеку.')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    class Meta:
        abstract = True


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    about = models.TextField()
    # team - поле для связи с командами в проектах/трекере
    # далее контакты, формат полей предварительный
    contact_telegram = models.CharField(max_length=50)
    contact_slack = models.CharField(max_length=50)
    contact_github = models.URLField()
