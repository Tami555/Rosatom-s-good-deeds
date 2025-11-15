from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Аутентификация волонтёров
    path('login/volunteer/', views.volunteer_login, name='volunteer_login'),
    path('register/volunteer/', views.volunteer_register, name='register_volunteer'),

    # Аутентификация НКО
    path('login/nko/', views.nko_login, name='nko_login'),
    path('register/nko/', views.nko_register, name='register_nko'),

    # Профиль
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('logout/', views.custom_logout, name='logout'),
]