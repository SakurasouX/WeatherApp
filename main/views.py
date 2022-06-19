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

    try:
        user_time = int(request.POST.get('user-time'))
    except TypeError:
        user_time = 0

    times = {}
    for x in range(len(data_list)):
        time = datetime.datetime.utcfromtimestamp(data_list[x]['dt'])
        times[x] = time

    city = data['city']
    city_name = city['name']
    city_country = city['country']

    sunrise_seconds = city['sunrise'] + city['timezone']
    sunset_seconds = city['sunset'] + city['timezone']
    sunrise_date = datetime.datetime.utcfromtimestamp(sunrise_seconds)
    sunset_date = datetime.datetime.utcfromtimestamp(sunset_seconds)
    sunrise = datetime.datetime.strftime(sunrise_date, '%H:%M')
    sunset = datetime.datetime.strftime(sunset_date, '%H:%M')
    day_length = sunset_date - sunrise_date

    city_timezone = city['timezone']
    local_time = datetime.datetime.now()
    time = datetime.timedelta(seconds=city_timezone - 10800) + local_time
    current_time = datetime.datetime.strftime(time, '%H:%M')

    temp_data = data_list[user_time]['main']
    temp = f"{temp_data['temp']:.0f}"
    feels_like = f"{temp_data['feels_like']:.0f}"
    weather = data_list[user_time]['weather'][0]['description'].title()
    clouds = data_list[user_time]['clouds']['all']
    wind = data_list[user_time]['wind']['speed']
    humidity = temp_data['humidity']
    pressure = temp_data['pressure']

    dt = data_list[user_time]['dt']
    weather_time = datetime.datetime.utcfromtimestamp(dt)
    weather_time_str = datetime.datetime.strftime(weather_time, '%H:%M')

    context = {
        'city_name': city_name,
        'city_country': city_country,
        'time': current_time,
        'sunrise': sunrise,
        'sunset': sunset,
        'day_length': day_length,
        'temp': temp,
        'feels_like': feels_like,
        'weather': weather,
        'clouds': clouds,
        'wind': wind,
        'humidity': humidity,
        'pressure': pressure,
        'weather_time': weather_time_str,
        'times': times,
    }

    return context
