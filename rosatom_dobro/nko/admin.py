from django.contrib import admin
from .models import City, Category, NKO


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(NKO)
class NKOAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'is_approved', 'has_access', 'created_at']
    list_filter = ['city', 'is_approved', 'has_access', 'category']
    search_fields = ['name', 'description']