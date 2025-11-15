from django.db import models
from nko.models import NKO


class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название события')
    description = models.TextField(verbose_name='Описание')
    start_date = models.DateTimeField(verbose_name='Дата начала')
    end_date = models.DateTimeField(verbose_name='Дата окончания')
    image = models.ImageField(upload_to='event_images/', blank=True, null=True, verbose_name='Изображение')
    address = models.TextField(blank=True, null=True, verbose_name='Адрес проведения')

    nko = models.ForeignKey(NKO, on_delete=models.CASCADE, verbose_name='НКО')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def is_active(self):
        from django.utils import timezone
        return self.end_date >= timezone.now()

    class Meta:
        verbose_name = 'Событие'
        verbose_name_plural = 'События'
        ordering = ['-start_date']