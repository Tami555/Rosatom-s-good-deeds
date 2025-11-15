from django.contrib import admin
from .models import Hashtag, KnowledgeBase


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title']
    list_per_page = 20


@admin.register(KnowledgeBase)
class KnowledgeBaseAdmin(admin.ModelAdmin):
    list_display = ['course_title', 'topic', 'speaker', 'created_at']
    list_filter = ['hashtags', 'created_at']
    search_fields = ['course_title', 'topic', 'speaker']
    filter_horizontal = ['hashtags']
    list_per_page = 20

    fieldsets = (
        ('Основная информация', {
            'fields': ('course_title', 'topic', 'speaker')
        }),
        ('Медиа', {
            'fields': ('video_url',)
        }),
        ('Теги', {
            'fields': ('hashtags',)
        }),
    )
