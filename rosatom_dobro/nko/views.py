from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import NKO, City, Category


def nko_list(request):
    # Получаем выбранный город из GET-параметра или сессии
    selected_city_id = request.GET.get('city') or request.session.get('selected_city')
    selected_category_id = request.GET.get('category')

    # Получаем все НКО
    nko_list = NKO.objects.filter(is_approved=True).select_related('city', 'category').prefetch_related('category')

    # Фильтрация по городу
    if selected_city_id:
        nko_list = nko_list.filter(city_id=selected_city_id)
        selected_city = get_object_or_404(City, id=selected_city_id)
    else:
        selected_city = None

    # Фильтрация по категории
    if selected_category_id:
        nko_list = nko_list.filter(category_id=selected_category_id)
        selected_category = get_object_or_404(Category, id=selected_category_id)
    else:
        selected_category = None

    # Поиск
    search_query = request.GET.get('search', '')
    if search_query:
        nko_list = nko_list.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(short_description__icontains=search_query)
        )

    # Сортировка
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'name':
        nko_list = nko_list.order_by('name')
    elif sort_by == 'city':
        nko_list = nko_list.order_by('city__name', 'name')

    # Пагинация
    paginator = Paginator(nko_list, 12)  # 12 карточек на страницу
    page = request.GET.get('page')

    try:
        nkos = paginator.page(page)
    except PageNotAnInteger:
        nkos = paginator.page(1)
    except EmptyPage:
        nkos = paginator.page(paginator.num_pages)

    # Контекст
    context = {
        'nkos': nkos,
        'cities': City.objects.all(),
        'categories': Category.objects.all(),
        'selected_city': selected_city,
        'selected_category': selected_category,
        'search_query': search_query,
        'sort_by': sort_by,
        'total_count': nko_list.count(),
    }

    return render(request, 'nko/nko_list.html', context)


def nko_detail(request, pk):
    nko = get_object_or_404(
        NKO.objects.select_related('city', 'category').prefetch_related('category'),
        pk=pk,
        is_approved=True
    )

    # Получаем похожие НКО (из того же города и категории)
    similar_nkos = NKO.objects.filter(
        city=nko.city,
        category=nko.category,
        is_approved=True
    ).exclude(pk=pk)[:4]

    context = {
        'nko': nko,
        'similar_nkos': similar_nkos,
    }

    return render(request, 'nko/nko_detail.html', context)