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
    local_time = datetime.datetime.now()
    time = datetime.timedelta(seconds=city_timezone - 10800) + local_time
    current_time = datetime.datetime.strftime(time, '%H:%M')

    for x in range(1):
        temp_data = data_list[x]['main']
        temp = f'{temp_data["temp"]:.0f}'
        feels_like = temp_data['feels_like']
        weather = data_list[x]['weather'][0]['description'].title()
        clouds = data_list[x]['clouds']
        wind = data_list[x]['wind']['speed']
        humidity = temp_data['humidity']
        pressure = temp_data['pressure']

    context = {
        'city_name': city_name,
        'city_country': city_country,
        'time': current_time,
        'sunrise': sunrise,
        'sunset': sunset,
        'temp': temp,
        'feels_like': feels_like,
        'weather': weather,
        'clouds': clouds,
        'wind': wind,
        'humidity': humidity,
        'pressure': pressure,
    }

    return context
