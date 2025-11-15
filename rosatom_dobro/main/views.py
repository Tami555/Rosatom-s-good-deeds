from django.shortcuts import render
from nko.models import City


def home(request):
    cities = City.objects.all()
    selected_city = request.session.get('selected_city')

    context = {
        'cities': cities,
        'selected_city': selected_city,
    }

    return render(request, 'main/home.html', context)