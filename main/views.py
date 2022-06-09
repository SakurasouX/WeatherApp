import requests
import datetime

from django.shortcuts import render

from .secret import API_KEY


def index(request):
    if request.method == 'POST':
        context = api_request(request)
        return render(request, 'main/index.html', context)
    else:
        return render(request, 'main/index.html')


def api_request(request):
    """
    Request an api weather site
    """
    user_city = request.POST.get('user_city')
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={user_city}&appid={API_KEY}&units=Metric&lang=ru'
    response = requests.get(url)

    if response.status_code == 404:
        return {'error': 'Ошибка сервера'}
    else:
        context = context_creator(request, response)
        return context


def context_creator(request, response):
    data = response.json()
    data_list = data['list']

    city = data['city']
    city_name = city['name']
    city_country = city['country']
    sunrise = city['sunrise']
    sunset = city['sunset']
    city_timezone = city['timezone']

    for x in range(1):
        temp_data = data_list[x]['main']
        temp = temp_data['temp']
        feels_like = temp_data['feels_like']
        weather = data_list[x]['weather']
        clouds = data_list[x]['clouds']
        wind = data_list[x]['wind']

    context = {
        'city_name': city_name,
        'city_country': city_country,
        'sunrise': sunrise,
        'sunset': sunset,
        'temp': temp,
        'feels_like': feels_like,
        'weather': weather,
        'clouds': clouds,
        'wind': wind,
        'time': city_timezone,
    }

    return context
