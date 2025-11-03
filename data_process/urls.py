# data_process/urls.py

from django.urls import path
from . import views

app_name = 'data_process'

urlpatterns = [
    path('collect-air-quality/', views.CollectAirQualityData.as_view(), name='collect_air_quality'),
    path('station-data/<str:station_id>/', views.GetStationData.as_view(), name='station_data'),
]