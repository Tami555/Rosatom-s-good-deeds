from django.shortcuts import render
from nko.models import City, NKO


def map_view(request):
    # Получаем выбранный город из GET-параметра или сессии
    selected_city_id = request.GET.get('city') or request.session.get('selected_city')

    # Получаем НКО для выбранного города
    if selected_city_id:
        nkos = NKO.objects.filter(city_id=selected_city_id, is_approved=True)
        selected_city = City.objects.get(id=selected_city_id)
    else:
        nkos = NKO.objects.filter(is_approved=True)
        selected_city = None

    context = {
        'cities': City.objects.all(),
        'selected_city': selected_city,
        'nkos': nkos,
        'nko_count': nkos.count(),
    }

    return render(request, 'map/map.html', context)