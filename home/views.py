from django.shortcuts import render
from django.http import JsonResponse
import requests
import json
import os

# AccuWeather API Configuration - Use environment variable for security
API_KEY = os.environ.get('ACCUWEATHER_API_KEY', 'zpka_9fda2bbaef414e97a4234daaa7437522_82653c5e')
BASE_URL = 'https://dataservice.accuweather.com'

def index(request):
    """Weather Dashboard - Main page"""
    return render(request, 'home/index.html', {'title': 'Weather Forecast'})

def search_location(request):
    """Search for a location and return location key"""
    query = request.GET.get('q', '')
    if not query:
        return JsonResponse({'error': 'No search query provided'}, status=400)
    
    try:
        url = f"{BASE_URL}/locations/v1/cities/search"
        params = {
            'apikey': API_KEY,
            'q': query,
            'language': 'en-us'
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        locations = response.json()
        
        # Format the response
        results = []
        for loc in locations[:5]:  # Limit to 5 results
            results.append({
                'key': loc.get('Key'),
                'name': loc.get('LocalizedName'),
                'country': loc.get('Country', {}).get('LocalizedName'),
                'region': loc.get('AdministrativeArea', {}).get('LocalizedName'),
            })
        return JsonResponse({'locations': results})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_current_weather(request):
    """Get current weather conditions for a location"""
    location_key = request.GET.get('location_key', '')
    if not location_key:
        return JsonResponse({'error': 'No location key provided'}, status=400)
    
    try:
        url = f"{BASE_URL}/currentconditions/v1/{location_key}"
        params = {
            'apikey': API_KEY,
            'details': 'true',
            'language': 'en-us'
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data and len(data) > 0:
            weather = data[0]
            result = {
                'temperature': {
                    'value': weather.get('Temperature', {}).get('Metric', {}).get('Value'),
                    'unit': '°C'
                },
                'feels_like': {
                    'value': weather.get('RealFeelTemperature', {}).get('Metric', {}).get('Value'),
                    'unit': '°C'
                },
                'weather_text': weather.get('WeatherText'),
                'weather_icon': weather.get('WeatherIcon'),
                'is_day': weather.get('IsDayTime'),
                'humidity': weather.get('RelativeHumidity'),
                'wind': {
                    'speed': weather.get('Wind', {}).get('Speed', {}).get('Metric', {}).get('Value'),
                    'direction': weather.get('Wind', {}).get('Direction', {}).get('Localized'),
                    'unit': 'km/h'
                },
                'uv_index': weather.get('UVIndex'),
                'uv_text': weather.get('UVIndexText'),
                'visibility': {
                    'value': weather.get('Visibility', {}).get('Metric', {}).get('Value'),
                    'unit': 'km'
                },
                'pressure': {
                    'value': weather.get('Pressure', {}).get('Metric', {}).get('Value'),
                    'unit': 'mb'
                },
                'cloud_cover': weather.get('CloudCover'),
                'observation_time': weather.get('LocalObservationDateTime'),
            }
            return JsonResponse({'weather': result})
        return JsonResponse({'error': 'No weather data available'}, status=404)
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_forecast(request):
    """Get 5-day weather forecast for a location"""
    location_key = request.GET.get('location_key', '')
    if not location_key:
        return JsonResponse({'error': 'No location key provided'}, status=400)
    
    try:
        url = f"{BASE_URL}/forecasts/v1/daily/5day/{location_key}"
        params = {
            'apikey': API_KEY,
            'metric': 'true',
            'details': 'true',
            'language': 'en-us'
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        forecasts = []
        for day in data.get('DailyForecasts', []):
            forecasts.append({
                'date': day.get('Date'),
                'temperature': {
                    'min': day.get('Temperature', {}).get('Minimum', {}).get('Value'),
                    'max': day.get('Temperature', {}).get('Maximum', {}).get('Value'),
                    'unit': '°C'
                },
                'day': {
                    'icon': day.get('Day', {}).get('Icon'),
                    'phrase': day.get('Day', {}).get('IconPhrase'),
                    'precipitation_probability': day.get('Day', {}).get('PrecipitationProbability'),
                },
                'night': {
                    'icon': day.get('Night', {}).get('Icon'),
                    'phrase': day.get('Night', {}).get('IconPhrase'),
                    'precipitation_probability': day.get('Night', {}).get('PrecipitationProbability'),
                },
                'sun': {
                    'rise': day.get('Sun', {}).get('Rise'),
                    'set': day.get('Sun', {}).get('Set'),
                },
                'hours_of_sun': day.get('HoursOfSun'),
            })
        
        headline = data.get('Headline', {}).get('Text', '')
        return JsonResponse({'forecasts': forecasts, 'headline': headline})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_hourly_forecast(request):
    """Get 12-hour weather forecast for a location"""
    location_key = request.GET.get('location_key', '')
    if not location_key:
        return JsonResponse({'error': 'No location key provided'}, status=400)
    
    try:
        url = f"{BASE_URL}/forecasts/v1/hourly/12hour/{location_key}"
        params = {
            'apikey': API_KEY,
            'metric': 'true',
            'details': 'true',
            'language': 'en-us'
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        hourly = []
        for hour in data:
            hourly.append({
                'datetime': hour.get('DateTime'),
                'temperature': {
                    'value': hour.get('Temperature', {}).get('Value'),
                    'unit': '°C'
                },
                'icon': hour.get('WeatherIcon'),
                'phrase': hour.get('IconPhrase'),
                'precipitation_probability': hour.get('PrecipitationProbability'),
                'is_daylight': hour.get('IsDaylight'),
            })
        
        return JsonResponse({'hourly': hourly})
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)

def about(request):
    """About page view"""
    return render(request, 'home/about.html', {'title': 'About Weather App'})
