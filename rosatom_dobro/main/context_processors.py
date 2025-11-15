from nko.models import City


def cities_processor(request):
    cities = City.objects.all()
    selected_city = request.session.get('selected_city')

    return {
        'cities': cities,
        'selected_city': selected_city,
    }