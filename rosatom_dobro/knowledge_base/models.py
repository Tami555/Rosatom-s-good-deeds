from django.db import models


class Hashtag(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class KnowledgeBase(models.Model):
    course_title = models.CharField(max_length=200, verbose_name='Название курса')
    topic = models.CharField(max_length=200, verbose_name='Тема')
    speaker = models.CharField(max_length=50, verbose_name='Спикер')
    video_url = models.URLField(blank=True, null=True, verbose_name='Ссылка на видео')
    created_at = models.DateTimeField(auto_now_add=True)
    hashtags = models.ManyToManyField(Hashtag, related_name='knowledge_bases')

    def __str__(self):
        return f'{self.course_title}; {self.topic}'

    class Meta:
        verbose_name = 'База знаний'
        verbose_name_plural = 'База знаний'