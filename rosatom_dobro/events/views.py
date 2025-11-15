from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.utils import timezone
from .models import Event
from .forms import EventCreateForm, EventUpdateForm
from nko.models import NKO


def event_list(request):
    # Получаем выбранный город из GET-параметра или сессии
    selected_city_id = request.GET.get('city') or request.session.get('selected_city')

    # Получаем события (только активные и будущие)
    now = timezone.now()
    events = Event.objects.filter(
        end_date__gte=now,
        nko__is_approved=True,
        nko__has_access=True
    ).select_related('nko', 'nko__city').order_by('start_date')

    # Фильтрация по городу
    if selected_city_id:
        events = events.filter(nko__city_id=selected_city_id)

    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(nko__name__icontains=search_query)
        )

    # Фильтрация по дате
    date_filter = request.GET.get('date_filter', 'upcoming')
    if date_filter == 'today':
        today = now.date()
        events = events.filter(start_date__date=today)
    elif date_filter == 'week':
        week_end = now + timezone.timedelta(days=7)
        events = events.filter(start_date__range=[now, week_end])
    elif date_filter == 'month':
        month_end = now + timezone.timedelta(days=30)
        events = events.filter(start_date__range=[now, month_end])

    # Пагинация
    paginator = Paginator(events, 8)  # 8 событий на страницу
    page = request.GET.get('page')

    try:
        events_page = paginator.page(page)
    except PageNotAnInteger:
        events_page = paginator.page(1)
    except EmptyPage:
        events_page = paginator.page(paginator.num_pages)

    context = {
        'events': events_page,
        'search_query': search_query,
        'date_filter': date_filter,
        'total_count': events.count(),
        'now': now,
    }

    return render(request, 'events/event_list.html', context)


def event_detail(request, pk):
    event = get_object_or_404(
        Event.objects.select_related('nko', 'nko__city'),
        pk=pk,
        nko__is_approved=True,
        nko__has_access=True
    )

    # Получаем похожие события от той же НКО
    similar_events = Event.objects.filter(
        nko=event.nko,
        end_date__gte=timezone.now()
    ).exclude(pk=pk)[:3]

    context = {
        'event': event,
        'similar_events': similar_events,
    }

    return render(request, 'events/event_detail.html', context)


@login_required
def event_create(request):
    # Проверяем, что пользователь - НКО и имеет доступ
    if not hasattr(request.user, 'nko') or not request.user.nko.has_access:
        messages.error(request, 'У вас нет прав для создания событий')
        return redirect('users:profile')

    nko = request.user.nko

    if request.method == 'POST':
        form = EventCreateForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.nko = nko
            event.save()
            messages.success(request, 'Событие успешно создано!')
            return redirect('events:event_list')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = EventCreateForm()

    context = {
        'form': form,
        'nko': nko,
    }

    return render(request, 'events/event_create.html', context)


@login_required
def event_edit(request, pk):
    # Проверяем, что пользователь - НКО и имеет доступ
    if not hasattr(request.user, 'nko') or not request.user.nko.has_access:
        messages.error(request, 'У вас нет прав для редактирования событий')
        return redirect('users:profile')

    event = get_object_or_404(Event, pk=pk, nko=request.user.nko)

    if request.method == 'POST':
        form = EventUpdateForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Событие успешно обновлено!')
            return redirect('events:event_manage')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = EventUpdateForm(instance=event)

    context = {
        'form': form,
        'event': event,
        'nko': request.user.nko,
    }

    return render(request, 'events/event_edit.html', context)


@login_required
def event_delete(request, pk):
    if not hasattr(request.user, 'nko') or not request.user.nko.has_access:
        messages.error(request, 'У вас нет прав для удаления событий')
        return redirect('users:profile')

    event = get_object_or_404(Event, pk=pk, nko=request.user.nko)

    if request.method == 'POST':
        event_title = event.title
        event.delete()
        messages.success(request, f'Событие "{event_title}" успешно удалено!')
        return redirect('events:event_manage')

    context = {
        'event': event,
    }

    return render(request, 'events/event_delete.html', context)


@login_required
def event_manage(request):
    # Проверяем, что пользователь - НКО
    if not hasattr(request.user, 'nko'):
        messages.error(request, 'Эта страница доступна только для НКО')
        return redirect('users:profile')

    nko = request.user.nko

    # Получаем события НКО с пагинацией
    events_list = Event.objects.filter(nko=nko).order_by('-created_at')

    # Фильтрация по статусу
    status_filter = request.GET.get('status', 'all')
    now = timezone.now()

    if status_filter == 'active':
        events_list = events_list.filter(end_date__gte=now)
    elif status_filter == 'past':
        events_list = events_list.filter(end_date__lt=now)
    elif status_filter == 'upcoming':
        events_list = events_list.filter(start_date__gt=now)

    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        events_list = events_list.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Пагинация
    paginator = Paginator(events_list, 10)
    page = request.GET.get('page')

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)

    # Статистика
    total_events = events_list.count()
    active_events = events_list.filter(end_date__gte=now).count()
    past_events = events_list.filter(end_date__lt=now).count()

    context = {
        'events': events,
        'nko': nko,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_events': total_events,
        'active_events': active_events,
        'past_events': past_events,
        'now': now,
    }

    return render(request, 'events/event_manage.html', context)