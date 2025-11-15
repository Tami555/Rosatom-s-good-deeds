from django.db import models
from django.conf import settings


class City(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class NKO(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название НКО')
    description = models.TextField(verbose_name='Описание деятельности')
    short_description = models.CharField(max_length=300, verbose_name='Краткое описание')
    logo = models.ImageField(upload_to='nko_logos/', blank=True, null=True, verbose_name='Логотип')
    address = models.TextField(blank=True, null=True, verbose_name='Адрес')
    website = models.URLField(blank=True, null=True, verbose_name='Сайт')
    vk_link = models.URLField(blank=True, null=True, verbose_name='ВКонтакте')
    telegram_link = models.URLField(blank=True, null=True, verbose_name='Telegram')

    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Категория', null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    is_approved = models.BooleanField(default=False, verbose_name='Подтверждено')
    has_access = models.BooleanField(default=False, verbose_name='Есть доступ к публикациям')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'НКО'
        verbose_name_plural = 'НКО'