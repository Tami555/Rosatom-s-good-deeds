from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import News
from nko.models import City


def news_list(request):
    # Получаем выбранный город из GET-параметра или сессии
    selected_city_id = request.GET.get('city') or request.session.get('selected_city')

    # Получаем новости
    news_list = News.objects.all().prefetch_related('cities')

    # Фильтрация по городу
    if selected_city_id:
        news_list = news_list.filter(cities__id=selected_city_id)
        selected_city = get_object_or_404(City, id=selected_city_id)
    else:
        selected_city = None

    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        news_list = news_list.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query)
        )

    # Пагинация
    paginator = Paginator(news_list, 8)  # 8 новостей на страницу
    page = request.GET.get('page')

    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    context = {
        'news': news,
        'search_query': search_query,
        'selected_city': selected_city,
        'total_count': news_list.count(),
    }

    return render(request, 'news/news_list.html', context)


def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)

    # Получаем похожие новости (из тех же городов)
    similar_news = News.objects.filter(
        cities__in=news.cities.all()
    ).exclude(pk=pk).distinct()[:3]

    context = {
        'news': news,
        'similar_news': similar_news,
    }

    return render(request, 'news/news_detail.html', context)