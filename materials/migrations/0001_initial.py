# Generated by Django 5.1.2 on 2024-10-30 11:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название.', max_length=100, verbose_name='Название курса')),
                ('description', models.TextField(help_text='Введите описание.', verbose_name='Описание курса')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Превью курса')),
            ],
            options={
                'verbose_name': 'Курс',
                'verbose_name_plural': 'Курсы',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Введите название.', max_length=100, verbose_name='Название урока')),
                ('description', models.TextField(help_text='Введите описание.', verbose_name='Описание урока')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Превью урока')),
                ('video_url', models.TextField(help_text='Прикрепите ссылку на видео для урока.', verbose_name='ссылка на видео')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.course', verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Урок',
                'verbose_name_plural': 'Уроки',
                'ordering': ['name', 'description', 'image', 'video_url'],
            },
        ),
    ]
