# Generated by Django 2.2.16 on 2022-09-13 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
                ('title', models.CharField(default='Заголовок', max_length=300, verbose_name='')),
                ('text', mdeditor.fields.MDTextField(verbose_name='Будьте конкретны. Представьте, что вы задаёте вопрос или пытаетесь продать что-то другому человеку.')),
                ('tags', models.CharField(blank=True, default='python;django;css;html', max_length=100, null=True)),
                ('github_link', models.URLField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
            ],
            options={
                'verbose_name': 'Идея проекта',
                'verbose_name_plural': 'Идеи проектов',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idea', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='team', to='ideas.Idea', verbose_name='Идея проекта')),
            ],
            options={
                'verbose_name': 'Команда',
                'verbose_name_plural': 'Команды',
            },
        ),
        migrations.CreateModel(
            name='TeamCandidates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='candidates', to='ideas.Team')),
            ],
        ),
        migrations.CreateModel(
            name='TeamUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ideas.Team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeamCandidatesUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('teamcandidates', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ideas.TeamCandidates')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='teamcandidates',
            name='users',
            field=models.ManyToManyField(related_name='users', through='ideas.TeamCandidatesUser', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(related_name='members', through='ideas.TeamUser', to=settings.AUTH_USER_MODEL, verbose_name='Участники'),
        ),
        migrations.AddField(
            model_name='team',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='teams', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Opinion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
                ('title', models.CharField(default='Заголовок', max_length=300, verbose_name='')),
                ('text', mdeditor.fields.MDTextField(verbose_name='Будьте конкретны. Представьте, что вы задаёте вопрос или пытаетесь продать что-то другому человеку.')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('idea', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opinions', to='ideas.Idea', verbose_name='Комментарий к этому проекту')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('-created',),
            },
        ),
    ]
