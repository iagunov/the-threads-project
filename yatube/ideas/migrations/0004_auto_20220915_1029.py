# Generated by Django 2.2.16 on 2022-09-15 10:29

from django.db import migrations
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0003_idea_who_needed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='who_needed',
            field=mdeditor.fields.MDTextField(default='Кто требуется в команду?'),
        ),
    ]
