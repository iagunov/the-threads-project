# Generated by Django 2.2.16 on 2022-09-14 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20220913_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='title',
            field=models.CharField(default='Заголовок', max_length=1000, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(default='Заголовок', max_length=1000, verbose_name=''),
        ),
    ]
