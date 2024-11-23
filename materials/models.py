from django.db import models

import users


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название курса', help_text="Введите название.")
    description = models.TextField(verbose_name='Описание курса', help_text="Введите описание.")
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='Превью курса')
    owner = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Владелец курса')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название урока', help_text="Введите название.")
    description = models.TextField(verbose_name='Описание урока', help_text="Введите описание.")
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='Превью урока')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='Курс')
    video_url = models.TextField(verbose_name='ссылка на видео', help_text="Прикрепите ссылку на видео для урока.")
    owner = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Владелец урока')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['name', 'description', 'image', 'video_url']


    def __str__(self):
        return self.name
