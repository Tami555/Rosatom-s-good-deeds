from django.urls import path
from . import views

app_name = 'knowledge_base'

urlpatterns = [
    path('', views.knowledge_list, name='knowledge_list'),
]