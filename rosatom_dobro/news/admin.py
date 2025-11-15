from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'show_photo', 'created_at']
    search_fields = ['title']

    @admin.display(description='Фотография')
    def show_photo(self, news: News):
        if news.image:
            return mark_safe(f'<img src={news.image.url} width=50px height=50px>')
        else:
            return 'Нет фотографии'