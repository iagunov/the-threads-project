from django.db import models
from mdeditor.fields import MDTextField

from core.models import Publication, User

class Tag(models.Model):
    name = models.CharField(
        null=True,
        blank=True,
        max_length=15
    )

    def __str__(self):
        return self.name

class Idea(Publication):
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='tags',
        through='TagIdea'
    )

    github_link = models.URLField(null=True, blank=True)

    who_needed = MDTextField(
        verbose_name='Кто нужен команде?',
        default='Перечислите в свободной форме',
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Идея проекта'
        verbose_name_plural = 'Идеи проектов'

    def __str__(self):
        return self.text[:15]

class TagIdea(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)

class Opinion(Publication):
    idea = models.ForeignKey(
        Idea,
        on_delete=models.CASCADE,
        verbose_name='Комментарий к этому проекту',
        related_name='opinions'
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]


class Team(models.Model):
    idea = models.OneToOneField(
        Idea,
        on_delete=models.CASCADE,
        verbose_name='Идея проекта',
        related_name='team'
    )
    members = models.ManyToManyField(
        User,
        verbose_name='Участники',
        related_name='members',
        through='TeamUser'
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='teams'
    )


    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'

class TeamCandidates(models.Model):
    team = models.OneToOneField(
        Team,
        on_delete=models.CASCADE,
        related_name='candidates'
    )
    users = models.ManyToManyField(
        User,
        related_name='users',
        through='TeamCandidatesUser'
    )

class TeamUser(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class TeamCandidatesUser(models.Model):
    teamcandidates = models.ForeignKey(TeamCandidates, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)