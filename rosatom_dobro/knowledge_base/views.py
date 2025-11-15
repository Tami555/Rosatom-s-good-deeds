from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db import models
from .models import KnowledgeBase, Hashtag


def knowledge_list(request):
    # Получаем выбранный хэштег из GET-параметра
    selected_hashtag_id = request.GET.get('hashtag')

    # Получаем все материалы базы знаний
    knowledge_list = KnowledgeBase.objects.all().prefetch_related('hashtags').order_by('-created_at')

    # Фильтрация по хэштегу
    if selected_hashtag_id:
        knowledge_list = knowledge_list.filter(hashtags__id=selected_hashtag_id)
        selected_hashtag = Hashtag.objects.get(id=selected_hashtag_id)
    else:
        selected_hashtag = None

    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        knowledge_list = knowledge_list.filter(
            Q(course_title__icontains=search_query) |
            Q(topic__icontains=search_query) |
            Q(speaker__icontains=search_query) |
            Q(hashtags__title__icontains=search_query)
        ).distinct()

    # Пагинация
    paginator = Paginator(knowledge_list, 9)  # 9 материалов на страницу
    page = request.GET.get('page')

    try:
        knowledge_items = paginator.page(page)
    except PageNotAnInteger:
        knowledge_items = paginator.page(1)
    except EmptyPage:
        knowledge_items = paginator.page(paginator.num_pages)

    # Получаем все хэштеги для фильтра
    all_hashtags = Hashtag.objects.all()

    # Получаем популярные хэштеги (те, которые чаще всего используются)
    popular_hashtags = Hashtag.objects.annotate(
        num_knowledge=models.Count('knowledge_bases')
    ).order_by('-num_knowledge')[:10]

    context = {
        'knowledge_items': knowledge_items,
        'all_hashtags': all_hashtags,
        'popular_hashtags': popular_hashtags,
        'selected_hashtag': selected_hashtag,
        'search_query': search_query,
        'total_count': knowledge_list.count(),
    }

    return render(request, 'knowledge_base/knowledge_list.html', context)