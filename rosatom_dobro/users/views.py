from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from .forms import (
    VolunteerRegistrationForm, NKORegistrationForm,
    CustomAuthenticationForm, UserUpdateForm, NKOUpdateForm
)
from .models import CustomUser
from nko.models import NKO


def volunteer_login(request):
    if request.user.is_authenticated:
        return redirect('users:profile')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None and user.user_type == 'volunteer':
                login(request, user)
                # messages.success(request, f'Добро пожаловать, {user.username}!')
                next_url = request.GET.get('next', 'users:profile')
                return redirect(next_url)
            else:
                messages.error(request, 'Неверные данные для входа или вы не волонтер')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = CustomAuthenticationForm()

    context = {
        'form': form,
        'user_type': 'volunteer',
        'title': 'Вход для волонтёров'
    }
    return render(request, 'users/login.html', context)


def nko_login(request):
    if request.user.is_authenticated:
        return redirect('users:profile')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None and user.user_type == 'nko':
                login(request, user)
                # messages.success(request, f'Добро пожаловать, {user.nko.name}!')
                next_url = request.GET.get('next', 'users:profile')
                return redirect(next_url)
            else:
                messages.error(request, 'Неверные данные для входа или вы не НКО')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = CustomAuthenticationForm()

    context = {
        'form': form,
        'user_type': 'nko',
        'title': 'Вход для НКО'
    }
    return render(request, 'users/login.html', context)


def volunteer_register(request):
    if request.user.is_authenticated:
        return redirect('users:profile')

    if request.method == 'POST':
        form = VolunteerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # messages.success(request, 'Регистрация прошла успешно! Добро пожаловать!')
            return redirect('users:profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = VolunteerRegistrationForm()

    context = {
        'form': form,
        'user_type': 'volunteer',
        'title': 'Регистрация волонтёра'
    }
    return render(request, 'users/register.html', context)


def nko_register(request):
    if request.user.is_authenticated:
        return redirect('users:profile')

    if request.method == 'POST':
        form = NKORegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # messages.success(request, 'Регистрация НКО прошла успешно! Ожидайте подтверждения администратора.')
            return redirect('users:profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = NKORegistrationForm()

    context = {
        'form': form,
        'user_type': 'nko',
        'title': 'Регистрация НКО'
    }
    return render(request, 'users/register.html', context)


@login_required
def profile(request):
    context = {}

    if request.user.user_type == 'nko':
        try:
            nko = NKO.objects.get(user=request.user)
            context['nko'] = nko
        except NKO.DoesNotExist:
            messages.error(request, 'Профиль НКО не найден')

    return render(request, 'users/profile.html', context)


@login_required
def profile_edit(request):
    if request.method == 'POST':
        if request.user.user_type == 'volunteer':
            form = UserUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Профиль успешно обновлен!')
                return redirect('users:profile')
        else:  # НКО
            nko = get_object_or_404(NKO, user=request.user)
            form = NKOUpdateForm(request.POST, request.FILES, instance=nko)
            if form.is_valid():
                form.save()
                messages.success(request, 'Профиль НКО успешно обновлен!')
                return redirect('users:profile')
    else:
        if request.user.user_type == 'volunteer':
            form = UserUpdateForm(instance=request.user)
        else:
            nko = get_object_or_404(NKO, user=request.user)
            form = NKOUpdateForm(instance=nko)

    context = {
        'form': form,
        'nko': getattr(request.user, 'nko', None) if request.user.user_type == 'nko' else None
    }
    return render(request, 'users/profile_edit.html', context)


@login_required
def custom_logout(request):
    logout(request)
    # messages.success(request, 'Вы успешно вышли из системы')
    return redirect('main:home')