from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('api/search/', views.search_location, name='search_location'),
    path('api/current/', views.get_current_weather, name='current_weather'),
    path('api/forecast/', views.get_forecast, name='forecast'),
    path('api/hourly/', views.get_hourly_forecast, name='hourly_forecast'),
]
