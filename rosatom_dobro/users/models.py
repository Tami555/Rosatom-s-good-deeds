from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('volunteer', 'Волонтер'),
        ('nko', 'НКО'),
        ('admin', 'Администратор'),
    )

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='volunteer')
    email = models.EmailField(unique=True, max_length=254, verbose_name='E-mail', db_index=True)
    age = models.IntegerField(blank=True, null=True)
    city = models.ForeignKey('nko.City', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.email})"
