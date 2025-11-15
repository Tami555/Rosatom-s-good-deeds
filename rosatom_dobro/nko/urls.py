from django.urls import path
from . import views

app_name = 'nko'

urlpatterns = [
    path('', views.nko_list, name='nko_list'),
    path('<int:pk>/', views.nko_detail, name='nko_detail'),
]